from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=500)
    authors = models.ManyToManyField(Author, related_name='books')
    pub_year = models.CharField(max_length=4)
    pages = models.PositiveSmallIntegerField()
    isbn_10 = models.CharField(max_length=10)
    isbn_13 = models.CharField(max_length=13)
    cover_url = models.URLField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
