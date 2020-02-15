from django import forms

from books.models import Author, Book


class BooksSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['authors', 'title', 'language']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        exclude = []


AuthorFormSet = forms.formset_factory(AuthorForm, extra=2)


class BooksAddForm(forms.ModelForm):
    language = forms.CharField()        # TODO use this to populate related model

    class Meta:
        model = Book
        exclude = ['authors']
