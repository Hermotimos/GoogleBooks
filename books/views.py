from django.shortcuts import render, redirect

from django.contrib import messages
from books.filters import BookFilter
from books.forms import BookForm, FirstAuthorForm, AuthorFormSet, LanguageForm
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
            print('not valid')

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
