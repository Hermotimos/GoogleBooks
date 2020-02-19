from django import forms

from books.models import Book
from books.utils import get_current_year, is_date_or_empty


YEARS_CHOICES = range(get_current_year(), 1450-1, -1)


class AuthorForm(forms.Form):
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Author'


AuthorFormSet = forms.formset_factory(AuthorForm, extra=3)


class FirstAuthorForm(AuthorForm):
    name = forms.CharField(max_length=100, required=True)


class LanguageForm(forms.Form):
    code = forms.CharField(min_length=2, max_length=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = '2-Digit language code'


class BookForm(forms.ModelForm):
    pages = forms.IntegerField(min_value=1, required=False)
    isbn = forms.CharField(min_length=13, max_length=13, required=False)
    pub_date = forms.CharField(
        required=False,
        widget=forms.SelectDateWidget(years=YEARS_CHOICES),
    )

    class Meta:
        model = Book
        exclude = ['authors', 'language', 'pub_date']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {'size': 70}
        self.fields['pub_date'].label = 'Publication date'
        self.fields['isbn'].label = 'ISBN'
        
    def clean_pub_date(self, *args, **kwargs):
        date = self.cleaned_data.get('pub_date')

        if len(date) == 0:
            date = ''
        else:
            date_list = date.split('-')
            year = date_list[0]
            month = date_list[1] if len(date_list) > 1 else 0
            day = date_list[2] if len(date_list) > 2 else 0
    
            if int(year) and int(month) and int(day):
                date = date
            elif int(year) and int(month):
                date = year + '-' + month
            elif int(year):
                date = year
            else:
                date = ''
                
            is_date_or_empty(date)
        return date


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
