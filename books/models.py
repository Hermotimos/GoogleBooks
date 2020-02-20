from django.db import models


class Author(models.Model):
    """Model for authors in authors-books many-to-many relationship."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name


class Language(models.Model):
    """Model for languages in languages-books many-to-many relationship."""
    code = models.CharField(max_length=2, unique=True)
    
    class Meta:
        ordering = ['code']

    def __str__(self):
        return self.code


class Book(models.Model):
    """Main model, has many-to-many relationships with Author and Language."""
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    pub_date = models.CharField(max_length=10, blank=True, null=True)
    pages = models.PositiveSmallIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    cover_url = models.URLField(unique=True, blank=True, null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,
                                 blank=True, null=True)

    class Meta:
        """
        Creates additional constraint and changes default ordering.
        
        Additional UNIQUE constraint is needed in db to avoid multiple entries
        with identical objects.
        """
        ordering = ['authors__name']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'pub_date', 'pages', 'cover_url'],
                name='unique-book-modalities',
            ),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Save blank field 'isbn' as None instead of empty string ''.
        
        Overrides default saving of blank fields as empty strings in database
        and enforces saving as NULLs (None is translated to NULL).
        Database treats two empty strings as equal, which isn't true for NULLs,
        so this override enables saving of multiple Book objects with 'isbn'
        field empty while using this field for UNIQUE check.
        """
        if not self.isbn:
            self.isbn = None
        super().save(*args, **kwargs)
