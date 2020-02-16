import django_filters

from books.models import Author, Book, Language


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = django_filters.ModelMultipleChoiceFilter(queryset=Language.objects.all())
    pub_date__gte = django_filters.NumberFilter(field_name='pub_date', lookup_expr='gte')
    pub_date__lte = django_filters.NumberFilter(field_name='pub_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'authors', 'language', 'pub_date__gte', 'pub_date__gte']
