import json

from django.shortcuts import render, redirect
from django.contrib import messages

import requests
from requests import Request

from books.filters import BookFilter
from books.forms import (BookForm, FirstAuthorForm, AuthorFormSet,
                         LanguageForm, BookImportForm)
from books.models import Author, Book, Language


def books_import_view(request):
    if request.method == 'POST':
        form = BookImportForm(data=request.POST)
        
        if form.is_valid():
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

                language_obj, _ = Language.objects.get_or_create(code=language)
                book, added = Book.objects.get_or_create(
                    title=title,
                    pub_date=pub_date,
                    pages=pages,
                    language=language_obj,
                    isbn=isbn,
                    cover_url=cover_url
                )
                if added:
                    added_cnt += 1
                    authors_objs = []
                    for name in authors_list:
                        author, _ = Author.objects.get_or_create(name=name)
                        authors_objs.append(author)
                    book.authors.set(authors_objs)

            messages.info(request,
                          f'{added_cnt} books added to your collection!')
    else:
        form = BookImportForm()

    context = {
        'form': form,
    }
    return render(request, 'books_import.html', context)


def books_list_view(request):
    books = Book.objects.all()
    filter_ = BookFilter(request.GET, queryset=books)

    context = {
        'books': books,
        'filter': filter_,
    }
    return render(request, 'books_list.html', context)


def books_add_view(request):
    if request.method == 'POST':
        first_author_form = FirstAuthorForm(data=request.POST)
        authors_fs = AuthorFormSet(data=request.POST)
        book_form = BookForm(data=request.POST)
        language_form = LanguageForm(data=request.POST)

        if (first_author_form.is_valid() and language_form.is_valid()
                and book_form.is_valid() and authors_fs.is_valid()):
            
            # referential integrity
            first_author_name = first_author_form.cleaned_data['name']
            first_author, _ \
                = Author.objects.get_or_create(name=first_author_name)

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

            # remaining fields
            year = book_form.cleaned_data['year']
            month = book_form.cleaned_data['month'] or None
            day = book_form.cleaned_data['day'] or None
            
            if month in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                month = '0' + month
            if day in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
                day = '0' + day

            if month and day:
                book.pub_date = str(year) + '-' + str(month) + '-' + str(day)
            elif month:
                book.pub_date = str(year) + '-' + str(month)
            else:
                book.pub_date = str(year)

            book.save()

            messages.info(request, f'New book has been added!')
            return redirect('add')
    else:
        first_author_form = FirstAuthorForm()
        authors_fs = AuthorFormSet()
        book_form = BookForm()
        language_form = LanguageForm()

    context = {
        'first_author_form': first_author_form,
        'authors_fs': authors_fs,
        'book_form': book_form,
        'language_form': language_form,
    }
    return render(request, 'books_add.html', context)
