from django_filters import rest_framework as filters
from rest_framework import viewsets

from books.api.serializers import AuthorSerializer, BookSerializer, LanguageSerializer
from books.models import Author, Book, Language


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    authors = filters.ModelMultipleChoiceFilter(queryset=Author.objects.all())
    language = filters.ModelMultipleChoiceFilter(queryset=Language.objects.all())
    pub_date__gte = filters.NumberFilter(field_name='pub_date', lookup_expr='gte')
    pub_date__lte = filters.NumberFilter(field_name='pub_date', lookup_expr='lte')

    class Meta:
        model = Book
        fields = ['title', 'authors', 'language', 'pub_date__gte', 'pub_date__lte']


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_class = BookFilter


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
