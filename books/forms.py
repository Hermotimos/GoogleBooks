from django import forms

from books.models import Book


class BooksSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['authors', 'title', 'language']


class BooksAddForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude = []
