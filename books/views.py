from django.shortcuts import render
from books.models import Author, Book, Language


def books_list_view(request):
    books = Book.objects.all()

    context = {
        'books': books
    }
    return render(request, 'books_list.html', context)


def books_add_view(request):
    pass