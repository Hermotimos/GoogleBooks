from django.test import TestCase
from django.urls import resolve, reverse

from books import views
from books.forms import BookImportForm
from books.models import Author, Book, Language


class BooksImportViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        """Provide url for tests."""
        cls.url = reverse('import')

    def test_get(self):
        """Status code of the HTTP response is 200."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_view(self):
        """URL is connected to specified view."""
        view = resolve('/import/')
        self.assertEqual(view.func, views.books_import_view)

    def test_csrf(self):
        """Response contains csrf token."""
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        """
        Response contains specified form, which is an instances of the
        corresponding form's class.
        """
        response = self.client.get(self.url)
        form = response.context.get('form')
        self.assertIsInstance(form, BookImportForm)

    def test_valid_post_data(self):
        """Valid data results in creation of database objects."""
        data = {
            'q': 'Hobbit',
            'intitle': '',
            'inauthor': '',
            'inpublisher': '',
            'subject': '',
            'isbn': '',
            'lccn': '',
            'oclc': '',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
    
        self.client.post(self.url, data)
    
        # As per 2010-02-19 => . data.py (Book: 40, Author: 36, Language: 2)
        # But this may vary; already observer Authors: 35 or 36.
        self.assertTrue(Book.objects.count() == 40)
        self.assertTrue(Author.objects.count() == 36)
        self.assertTrue(Language.objects.count() == 2)

    def test_invalid_post_data(self):
        """
        Invalid data does not redirect, shows the form again with
        validation errors, and does not result in creation of any objects.
        """
        data = {
            'q': 'Hobbit',
            'intitle': '',
            'inauthor': '',
            'inpublisher': '',
            'subject': '',
            'isbn': '12121212121212121212',     # > max_length=13
            'lccn': '',
            'oclc': '',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        
        form = response.context.get('form')
        self.assertTrue(form.errors)
        
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
    def test_invalid_post_data_empty_fields(self):
        """
        Invalid data (empty fields) does not redirect, shows the form again
        with validation errors, and does not result in creation of any objects.
        """
        data = {
            'q': '',
            'intitle': '',
            'inauthor': '',
            'inpublisher': '',
            'subject': '',
            'isbn': '',
            'lccn': '',
            'oclc': '',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
        response = self.client.post(self.url, data)
        self.assertEquals(response.status_code, 200)
        
        form = response.context.get('form')
        self.assertTrue(form.errors)
        
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
