from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Language(models.Model):
    code = models.CharField(max_length=2, unique=True)
    
    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    pub_date = models.CharField(max_length=10, blank=True, null=True)
    pages = models.PositiveSmallIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    cover_url = models.URLField(blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 blank=True, null=True)

    class Meta:
        """Put constraint on combination of model fields.
        
        Ex. https://www.googleapis.com/books/v1/volumes?q=Hobbit
        results in multiple imports of:
        'John Ronald Reuel Tolkien, Hobbit czyli Tam i z powrotem,
        pub. 1985, pp. 233 [pl] '
        """
        ordering = ['authors__name']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'pub_date', 'pages', 'cover_url'],
                name='unique-book-modalities',
            )
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Save blank 'isbn' field as None (NULL in db) instead of ''.
        
        Overrides default saving of blank fields as empty strings.
        Database treats two empty strings as equal, which isn't true for NULLs.
        This override enables saving multiple Book objects without ISBN
        while using 'isbn' for UNIQUE check in the database.
        """
        if not self.isbn:
            self.isbn = None
        super().save(*args, **kwargs)
