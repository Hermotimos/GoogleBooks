import json

from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect

import requests
from requests import Request

from books.filters import BookFilter
from books.forms import (BookForm, FirstAuthorForm, AuthorFormSet,
                         LanguageForm, BookImportForm)
from books.models import Author, Book, Language


def books_list_view(request):
    books = Book.objects.all()
    filter_ = BookFilter(request.GET, queryset=books)

    context = {
        'books': books,
        'filter': filter_,
    }
    return render(request, 'books_list.html', context)


def books_add_view(request):
    first_author_form = FirstAuthorForm(data=request.POST or None)
    authors_fs = AuthorFormSet(data=request.POST or None)
    book_form = BookForm(data=request.POST or None)
    language_form = LanguageForm(data=request.POST or None)

    if (first_author_form.is_valid() and language_form.is_valid()
            and book_form.is_valid() and authors_fs.is_valid()):
        
        # referential integrity
        first_author_name = first_author_form.cleaned_data['name']
        first_author, _ = Author.objects.get_or_create(name=first_author_name)

        more_authors = []
        for form in authors_fs:
            try:
                author_name = form.cleaned_data['name']
                author, _ = Author.objects.get_or_create(name=author_name)
                more_authors.append(author)
            except KeyError:
                pass

        language_code = language_form.cleaned_data['code']
        language, _ = Language.objects.get_or_create(code=language_code)

        book = book_form.save(commit=False)
        book.language = language
        book = book_form.save()
        book.authors.add(first_author)
        if more_authors:
            book.authors.add(*list(more_authors))

        # pub_date
        date = book_form.cleaned_data['pub_date']
        try:
            [year, month, day] = date.split('-')
        
            if int(year) and int(month) and int(day):
                book.pub_date = date
            elif int(year) and int(month):
                book.pub_date = year + '-' + month
            elif int(year):
                book.pub_date = year
            else:
                book.pub_date = ''
        except ValueError:
            book.pub_date = ''
        
        book.save()

        messages.info(request, f'New book has been added!')
        return redirect('add')

    context = {
        'first_author_form': first_author_form,
        'authors_fs': authors_fs,
        'book_form': book_form,
        'language_form': language_form,
    }
    return render(request, 'books_add.html', context)


def books_import_view(request):
    books_list = []
    if request.method == 'POST':
        form = BookImportForm(data=request.POST)
        
        if form.is_valid():
            # ----- Retrieve JSON data from API -----
            terms = {}
            for k, v in form.cleaned_data.items():
                if v:
                    terms[k] = v
            
            req = Request('POST',
                          'https://www.googleapis.com/books/v1/volumes',
                          params=terms)
            prep = req.prepare()
            url = prep.url.replace('&', '+')
            response = requests.get(url)
            
            # ----- Parse JSON data -----
            data = json.loads(response.text)
            added_cnt = 0
            for item in data['items']:
                try:
                    title = item['volumeInfo']['title']
                except KeyError:
                    title = ''
                
                try:
                    authors_list = item['volumeInfo']['authors']
                except KeyError:
                    authors_list = []
                
                try:
                    pub_date = item['volumeInfo']['publishedDate']
                except KeyError:
                    pub_date = ''
                
                try:
                    pages = item['volumeInfo']['pageCount']
                except KeyError:
                    pages = None
                
                isbn = ''
                try:
                    for elem in item['volumeInfo']['industryIdentifiers']:
                        if elem['type'] == 'ISBN_13':
                            isbn = elem['identifier']
                            break
                        elif elem['type'] == 'ISBN_10':
                            isbn = elem['identifier']
                except KeyError:
                    isbn = ''
                
                try:
                    language = item['volumeInfo']['language']
                except KeyError:
                    language = ''
                
                try:
                    cover_url = item['volumeInfo']['imageLinks']['thumbnail']
                except KeyError:
                    cover_url = ''
                
                # ----- Populate database with parsed data -----
                
                try:
                    book, added = Book.objects.get_or_create(
                        title=title,
                        pub_date=pub_date,
                        pages=pages,
                        isbn=isbn,
                        cover_url=cover_url
                    )
                    if added:
                        added_cnt += 1
                        
                        language_obj, _ = Language.objects.get_or_create(
                            code=language)
                        book.language = language_obj
                        
                        authors_objs = []
                        for name in authors_list:
                            author, _ = Author.objects.get_or_create(name=name)
                            authors_objs.append(author)
                        book.authors.set(authors_objs)
                        
                        books_list.append(book)
                        print(books_list)
                except IntegrityError:
                    pass
            
            messages.info(
                request,
                f'You have added {added_cnt} books to your collection!'
            )
    else:
        form = BookImportForm()
    
    context = {
        'form': form,
        'books_list': books_list
    }
    return render(request, 'books_import.html', context)
