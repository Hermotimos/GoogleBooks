from rest_framework import serializers

from books.models import Author, Book, Language


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        # fields = [
        #     'title',
        #     'authors',
        #     'pub_date',
        #     'pages',
        #     'isbn',
        #     'cover_url',
        #     'language',
        # ]
        fields = '__all__'
        

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'
