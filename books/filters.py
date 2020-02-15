import django_filters

from books.models import Author, Book, Language


class BookFilter(django_filters.FilterSet):
    authors = django_filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = django_filters.ModelMultipleChoiceFilter(queryset=Language.objects.all())

    class Meta:
        model = Book
        fields = {
            'title': ['icontains'],
            'authors': [],
            'language': [],
            'pub_year': ['lte', 'gte']
        }
