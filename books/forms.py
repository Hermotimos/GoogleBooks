from django import forms

from books.models import Book
from books.utils import get_current_year, get_date_or_empty


YEARS_CHOICES = range(get_current_year(), 1450-1, -1)


class AuthorForm(forms.Form):
    """A form for searching by author and adding authors to database."""
    name = forms.CharField(max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Author'


AuthorFormSet = forms.formset_factory(AuthorForm, extra=3)


class LanguageForm(forms.Form):
    """A form for searching by language and adding languages to database."""
    code = forms.CharField(min_length=2, max_length=2)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = '2-Digit language code'


class BookForm(forms.ModelForm):
    """A form for searching by Book fields and adding books to database."""
    pages = forms.IntegerField(min_value=1, required=False)
    isbn = forms.CharField(max_length=13, required=False)
    pub_date = forms.CharField(
        required=False,
        widget=forms.SelectDateWidget(years=YEARS_CHOICES),
    )

    class Meta:
        model = Book
        exclude = ['authors', 'language', 'pub_date']

    def __init__(self, *args, **kwargs):
        """Override fields' labels and size."""
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].label = 'Publication date'
        self.fields['isbn'].label = 'ISBN'

    def clean_pub_date(self, *args, **kwargs):
        """Return date input from pub_date field as valid date or empty str."""
        date = self.cleaned_data.get('pub_date')
        date = get_date_or_empty(date)
        return date


class BookImportForm(forms.Form):
    """Form for importing volumes by keywords from Google Books API v1."""
    q = forms.CharField()
    intitle = forms.CharField(required=False)
    inauthor = forms.CharField(required=False)
    inpublisher = forms.CharField(required=False)
    subject = forms.CharField(required=False)
    isbn = forms.CharField(max_length=13, required=False)
    lccn = forms.CharField(required=False)
    oclc = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        """Override fields' labels and size."""
        super().__init__(*args, **kwargs)
        self.fields['q'].label = 'Keyword(s):'
        self.fields['intitle'].label = 'In title:'
        self.fields['inauthor'].label = 'In author:'
        self.fields['inpublisher'].label = 'In publisher:'
        self.fields['subject'].label = 'In category:'
        self.fields['isbn'].label = 'ISBN:'
        self.fields['lccn'].label = '<small>' \
                                    'Library of Congress Control No.:' \
                                    '</small>'
        self.fields['oclc'].label = '<small>' \
                                    'Online Computer Library Center No.:' \
                                    '</small>'
