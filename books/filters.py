import django_filters as filters

from books.models import Author, Language


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.all()
    )
    pub_date_between = filters.DateFromToRangeFilter(
        field_name='pub_date',
        label='Date (From - To) yyyy-mm-dd',
    )
