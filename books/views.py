from django.shortcuts import render

from books.forms import BooksSearchForm, BooksAddForm
from books.models import Author, Book, Language


def books_list_view(request):
    books = Book.objects.all()

    form = BooksSearchForm()

    context = {
        'books': books,
        'form': form
    }
    return render(request, 'books_list.html', context)


def books_add_view(request):
    form = BooksAddForm()
    context = {
        'form': form
    }

    return render(request, 'books_add.html', context)