from django.contrib import admin
from books.models import Author, Book, Language

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Language)
