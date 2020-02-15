import django_filters

from books.models import Author, Book, Language


class BookFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains')
    authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = django_filters.ModelMultipleChoiceFilter(queryset=Language.objects.all())
    pub_year__gte = django_filters.NumberFilter(field_name='pub_year', lookup_expr='gte')
    pub_year__lte = django_filters.NumberFilter(field_name='pub_year', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'authors', 'language', 'pub_year__gte', 'pub_year__gte']
