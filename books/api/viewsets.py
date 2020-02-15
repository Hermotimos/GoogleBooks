from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from books.api.serializers import AuthorSerializer, BookSerializer, LanguageSerializer
from books.models import Author, Book, Language


# class BookList(APIView):
#
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True, context={'request': request})
#         return Response(serializer.data)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
