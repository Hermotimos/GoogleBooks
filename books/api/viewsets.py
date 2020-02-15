from django_filters import rest_framework as filters
from rest_framework import viewsets

from books.api.serializers import AuthorSerializer, BookSerializer, LanguageSerializer
from books.models import Author, Book, Language


# class AuthorFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = Author
#         fields = ['name']


class BookFilter(filters.FilterSet):

    # TODO add pub_date and DateFromToRangeFilter (requires DateField)

    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.ModelMultipleChoiceFilter(field_name='authors__name',  to_field_name='name',
                                                queryset=Author.objects.all())

    class Meta:
        model = Book
        fields = ['title', 'authors', 'language']   # TODO add pub_date and DateFromToRangeFilter (requires DateField)


# class LanguageFilter(filters.FilterSet):
#     name = filters.CharFilter(lookup_expr='icontains')
#
#     class Meta:
#         model = Language
#         fields = ['name']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # filterset_class = AuthorFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_fields = ['title']
    filterset_class = BookFilter


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    # filterset_class = LanguageFilter
