from django.shortcuts import render, redirect

from django.contrib import messages
from books.filters import BookFilter
from books.forms import BooksSearchForm, BookForm, FirstAuthorForm, AuthorFormSet, LanguageForm
from books.models import Author, Book, Language
from books_project.utils import query_debugger


@query_debugger
def books_list_view(request):
    books = Book.objects.all()
    form = BooksSearchForm()
    filter_ = BookFilter(request.GET, queryset=books)

    context = {
        'books': books,
        'form': form,
        'filter': filter_
    }
    return render(request, 'books_list.html', context)


@query_debugger
def books_add_view(request):
    if request.method == 'POST':
        first_author_form = FirstAuthorForm(data=request.POST)
        # authors_formset = AuthorFormSet(data=request.POST)
        book_form = BookForm(data=request.POST)
        language_form = LanguageForm(data=request.POST)

        if first_author_form.is_valid() and language_form.is_valid():
            first_author_name = first_author_form.cleaned_data['name']
            first_author, _ = Author.objects.get_or_create(name=first_author_name)

            language_code = language_form.cleaned_data['code']
            language, _ = Language.objects.get_or_create(code=language_code)

            book = book_form.save(commit=False)
            book.language = language
            book = book_form.save()
            book.authors.add(first_author)
            # if more_authors:
            #     book.authors.add(*list(more_authors))

            print(book_form.cleaned_data)

            year = book_form.cleaned_data['year']
            month = book_form.cleaned_data['month'] or None
            day = book_form.cleaned_data['day'] or None

            if month and day:
                book.pub_year = str(year) + '-' + str(month) + '-' + str(day)
            elif month:
                book.pub_year = str(year) + '-' + str(month)
            else:
                book.pub_year = str(year)

            book.save()

            messages.info(request, f'New book has been added!')
            return redirect('add')
        else:
            print('not valid')

    else:
        first_author_form = FirstAuthorForm()
        # authors_formset = AuthorFormSet()
        book_form = BookForm()
        language_form = LanguageForm()

    context = {
        'first_author_form': first_author_form,
        # 'authors_formset': authors_formset,
        'book_form': book_form,
        'language_form': language_form
    }
    return render(request, 'books_add.html', context)
