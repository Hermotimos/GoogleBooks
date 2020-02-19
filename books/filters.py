import django_filters as filters

from books.models import Author, Language


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.all()
    )
    pub_date_range = filters.DateFromToRangeFilter(
        field_name='pub_date',
        label='Date After (excluded) - Before (included) as YYYY-MM-DD',
    )
