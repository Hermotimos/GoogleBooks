from django.test import TestCase
from django.urls import resolve, reverse

from books import views
from books.forms import (AuthorForm, AuthorFormSet, BookForm,
                         LanguageForm)
from books.models import Author, Book, Language


class BooksAddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.url = reverse('add')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_url_resolves_view(self):
        view = resolve('/add/')
        self.assertEqual(view.func, views.books_add_view)

    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'csrfmiddlewaretoken')
        
    def test_contains_forms(self):
        response = self.client.get(self.url)
        
        first_author_form = response.context.get('first_author_form')
        authors_fs = response.context.get('authors_fs')
        book_form = response.context.get('book_form')
        language_form = response.context.get('language_form')
        
        self.assertIsInstance(first_author_form, AuthorForm)
        self.assertIsInstance(authors_fs, AuthorFormSet)
        self.assertIsInstance(book_form, BookForm)
        self.assertIsInstance(language_form, LanguageForm)

    def test_valid_post_data(self):
        data = {
            # first_author_form
            'name': 'Test author 1',
            
            # authors_fs --> 'form-0-name', ..., 'form-3-name' + ManagementForm
            'form-0-name': 'Test author 2',
            'form-1-name': '',
            'form-2-name': '',
            'form-3-name': '',
            'form-TOTAL_FORMS': ['4'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['0'],
            'form-MAX_NUM_FORMS': ['1000'],
            
            # language_form
            'code': 'xx',
            
            # book_form
            'title': 'Test title 1',
            'pub_date': '2000',
            'pages': '200',
            'isbn': '9780575079212',
            'cover_url': 'http://127.0.0.1:8000/',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
        self.client.post(self.url, data)
        
        self.assertTrue(Book.objects.count() == 1)
        self.assertTrue(Author.objects.count() == 2)
        self.assertTrue(Language.objects.count() == 1)

    def test_invalid_post_data(self):
        data = {
            # first_author_form
            'name': 'len(name) > 100' * 100,
        
            # authors_fs --> 'form-0-name', ..., 'form-3-name' + ManagementForm
            'form-0-name': 'len(name) > 100' * 100,
            'form-1-name': '',
            'form-2-name': '',
            'form-3-name': '',
            'form-TOTAL_FORMS': ['4'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['0'],
            'form-MAX_NUM_FORMS': ['1000'],
        
            # language_form
            'code': 'len(str) > 2',
        
            # book_form
            'title': 'len(title) > 500' * 500,
            'pub_date': '2500',
            'pages': '-200',
            'isbn': '11111111111111111111',
            'cover_url': 'not an url',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
        response = self.client.post(self.url, data)
        
        # should show the form again, not redirect
        self.assertEquals(response.status_code, 200)
        
        first_author_form = response.context.get('first_author_form')
        authors_fs = response.context.get('authors_fs')
        language_form = response.context.get('language_form')
        book_form = response.context.get('book_form')

        self.assertTrue(first_author_form.errors)
        self.assertTrue(authors_fs.errors)
        self.assertTrue(language_form.errors)
        self.assertTrue(book_form.errors)

        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
    def test_invalid_post_data_empty_fields(self):
        data = {
            # first_author_form
            'name': '',
        
            # authors_fs --> 'form-0-name', ..., 'form-3-name' + ManagementForm
            'form-0-name': '',
            'form-1-name': '',
            'form-2-name': '',
            'form-3-name': '',
            'form-TOTAL_FORMS': ['4'],
            'form-INITIAL_FORMS': ['0'],
            'form-MIN_NUM_FORMS': ['0'],
            'form-MAX_NUM_FORMS': ['1000'],
        
            # language_form
            'code': '',
        
            # book_form
            'title': '',
            'pub_date': '',
            'pages': '',
            'isbn': '',
            'cover_url': '',
        }
        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
        
        response = self.client.post(self.url, data)
        
        # should show the form again, not redirect
        self.assertEquals(response.status_code, 200)
        
        language_form = response.context.get('language_form')
        book_form = response.context.get('book_form')
        self.assertTrue(language_form.errors)
        self.assertTrue(book_form.errors)

        self.assertTrue(Book.objects.count() == 0)
        self.assertTrue(Author.objects.count() == 0)
        self.assertTrue(Language.objects.count() == 0)
