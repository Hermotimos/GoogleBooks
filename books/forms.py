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


AuthorFormSet = forms.formset_factory(AuthorForm, extra=2)


class BooksAddForm(forms.ModelForm):
    authors = forms.CharField(max_length=100)
    language = forms.CharField(max_length=2)        # TODO use this to populate related model

    class Meta:
        model = Book
        exclude = []

    def __init__(self, *args, **kwargs):
        super(BooksAddForm, self).__init__(*args, **kwargs)
        self.fields['authors'].label = 'Author'

        self.fields['title'].widget.attrs = {'size': 70}
