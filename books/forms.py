import datetime

from django import forms

from books.models import Author, Book, Language


class FirstAuthorForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Author'


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Author'


AuthorFormSet = forms.formset_factory(AuthorForm, extra=4)


class LanguageForm(forms.Form):
    code = forms.CharField(min_length=2, max_length=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = '2-Digit language code'


def get_current_year():
    return datetime.datetime.now().year


class BookForm(forms.ModelForm):
    pages = forms.IntegerField(min_value=1)
    isbn_10 = forms.CharField(min_length=10, max_length=10)
    isbn_13 = forms.CharField(min_length=13, max_length=13)

    year = forms.IntegerField(min_value=1450, max_value=get_current_year)
    month = forms.IntegerField(min_value=1, max_value=12, required=False)
    day = forms.IntegerField(min_value=1, max_value=31, required=False)

    class Meta:
        model = Book
        exclude = ['authors', 'language', 'pub_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'size': 70}
