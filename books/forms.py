import datetime

from django import forms

from books.models import Book


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


AuthorFormSet = forms.formset_factory(AuthorForm, extra=3)


class LanguageForm(forms.Form):
    code = forms.CharField(min_length=2, max_length=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = '2-Digit language code'


def get_current_year():
    return datetime.datetime.now().year


class BookForm(forms.ModelForm):
    pages = forms.IntegerField(min_value=1)
    isbn = forms.CharField(min_length=13, max_length=13)

    year = forms.IntegerField(min_value=1450, max_value=get_current_year)
    month = forms.IntegerField(min_value=1, max_value=12, required=False)
    day = forms.IntegerField(min_value=1, max_value=31, required=False)

    class Meta:
        model = Book
        exclude = ['authors', 'language', 'pub_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'size': 70}


class BookImportForm(forms.Form):
    q = forms.CharField()
    intitle = forms.CharField(required=False)
    inauthor = forms.CharField(required=False)
    inpublisher = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    isbn = forms.CharField(max_length=13, required=False)
    lccn = forms.CharField(required=False)
    oclc = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['q'].label = 'Keyword(s):'
        self.fields['q'].widget.attrs = {'size': 25}
        
        self.fields['intitle'].label = 'In title:'
        self.fields['intitle'].widget.attrs = {'size': 25}
        
        self.fields['inauthor'].label = 'In author:'
        self.fields['inauthor'].widget.attrs = {'size': 25}
        
        self.fields['inpublisher'].label = 'In publisher:'
        self.fields['inpublisher'].widget.attrs = {'size': 25}
        
        self.fields['subject'].label = 'In category:'
        self.fields['subject'].widget.attrs = {'size': 25}
        
        self.fields['isbn'].label = 'ISBN:'
        self.fields['isbn'].widget.attrs = {'size': 25}
        
        self.fields['lccn'].label = 'Library of Congress Control Number:'
        self.fields['lccn'].widget.attrs = {'size': 25}
        
        self.fields['oclc'].label = 'Online Computer Library Center number:'
        self.fields['oclc'].widget.attrs = {'size': 25}
