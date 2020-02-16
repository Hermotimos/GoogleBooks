import datetime
from django import forms

from books.models import Author, Book


class BooksSearchForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['authors', 'title', 'language']


class AuthorForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = Author
        exclude = []

    def __init__(self, *args, **kwargs):
        super(AuthorForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = 'Author'


AuthorFormSet = forms.formset_factory(AuthorForm, extra=4)


def get_current_year():
    return datetime.datetime.now().year


class BooksAddForm(forms.ModelForm):
    authors = forms.CharField(max_length=100)
    pages = forms.IntegerField(min_value=1)
    language = forms.CharField(min_length=2, max_length=2)        # TODO use this to populate related model
    isbn_10 = forms.CharField(min_length=10, max_length=10)
    isbn_13 = forms.CharField(min_length=13, max_length=13)

    year = forms.IntegerField(min_value=1450, max_value=get_current_year)
    month = forms.IntegerField(min_value=1, max_value=12)
    day = forms.IntegerField(min_value=1, max_value=31)

    class Meta:
        model = Book
        exclude = ['pub_year']

    def __init__(self, *args, **kwargs):
        super(BooksAddForm, self).__init__(*args, **kwargs)
        self.fields['authors'].label = 'Author'

        self.fields['title'].widget.attrs = {'size': 70}
