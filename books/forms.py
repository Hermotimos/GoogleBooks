from django import forms

from books.models import Book


class BookAddForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []
