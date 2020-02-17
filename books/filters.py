import django_filters as filters

from books.models import Author, Book, Language


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.ModelMultipleChoiceFilter(
        queryset=Author.objects.all())
    language = filters.ModelMultipleChoiceFilter(
        queryset=Language.objects.all())
    pub_date__gte = filters.NumberFilter(field_name='pub_date',
                                         lookup_expr='gte')
    pub_date__lte = filters.NumberFilter(field_name='pub_date',
                                         lookup_expr='lte')

    class Meta:
        model = Book
        fields = [
            'title',
            'authors',
            'language',
            'pub_date__gte',
            'pub_date__gte',
        ]
