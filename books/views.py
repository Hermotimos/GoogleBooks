from django.shortcuts import render

from books.filters import BookFilter
from books.forms import BooksSearchForm, BooksAddForm
from books.models import Book


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


def books_add_view(request):
    form = BooksAddForm()
    context = {
        'form': form
    }

    return render(request, 'books_add.html', context)