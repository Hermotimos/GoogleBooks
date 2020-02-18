from django.test import TestCase
from django.urls import resolve, reverse

from books import views
from books.filters import BookFilter
from books.forms import (FirstAuthorForm, AuthorFormSet, BookForm,
                         LanguageForm)
from books.models import Author, Book, Language


class BooksListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author_1 = Author.objects.create(name='Test author 1')
        cls.author_2 = Author.objects.create(name='Test author 2')
        
        cls.language_1 = Language.objects.create(code='xx')
        cls.language_2 = Language.objects.create(code='yy')
        
        cls.book_1 = Book.objects.create(
            title='Test title 1',
            pub_date='2000',
            pages=200,
            isbn='9780575079212',
            cover_url='https://www.abebooks.com/book-search/author/'
                      'PHILIP-K-DICK?cm_sp=brcr-_-bdp-_-author',
            language=cls.language_1
        )
        cls.book_2 = Book.objects.create(
            title='Title test 2',
            pub_date='1999',
            pages=199,
            isbn='9788834730317',
            cover_url='https://www.abebooks.com/9788834730317/'
                      'Ubik-8834730313/plp',
            language=cls.language_2
        )
        cls.book_1.authors.add(cls.author_1)
        cls.book_2.authors.add(cls.author_2)
        
        cls.url = reverse('list')
        
    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        
    def test_url_resolves_view(self):
        view = resolve('/')
        self.assertEqual(view.func, views.books_list_view)
        
    def test_contains(self):
        response = self.client.get(self.url)
        
        for book in Book.objects.all():
            for auth in book.authors.all():
                self.assertContains(response, auth.name)
            self.assertContains(response, book.title)
            self.assertContains(response, book.pub_date)
            self.assertContains(response, book.pages)
            self.assertContains(response, book.isbn)
            self.assertContains(response, book.cover_url)
            self.assertContains(response, book.language.code)

    def test_filters(self):
        books = Book.objects.all()
        
        def check_filtering(test_case, obj, included_qs, excluded_qs):
            test_case.assertTrue(obj in included_qs)
            for o in excluded_qs:
                self.assertTrue(o not in included_qs)
        
        for book in books:
            
            # Test filter by title
            in_title = book.title[:-1]
            f = BookFilter(data={'title': in_title}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(title__icontains=in_title)
            check_filtering(self, book, in_qs, out_qs)
            
            # Test filter by language
            language_id = book.language.id
            f = BookFilter(data={'language': [language_id]}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(language_id=language_id)
            check_filtering(self, book, in_qs, out_qs)

            # Test filter by author
            author_id = book.authors.first().id
            f = BookFilter(data={'authors': [author_id]}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(authors__in=
                                          [a for a in book.authors.all()])
            check_filtering(self, book, in_qs, out_qs)

            # Test filter by pud_date
            gte = book.pub_date
            f = BookFilter(data={'pub_date__gte': gte}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(pub_date__gte=gte)
            check_filtering(self, book, in_qs, out_qs)
            
            lte = str(int(book.pub_date) + 1)
            f = BookFilter(data={'pub_date__gte': gte, 'pub_date__lte': lte},
                           queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(pub_date__gte=gte, pub_date__lte=lte)
            check_filtering(self, book, in_qs, out_qs)


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
        
        self.assertIsInstance(first_author_form, FirstAuthorForm)
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
            'year': '2000',
            'month': '',
            'day': '',
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
            'year': '2500',
            'month': '',
            'day': '',
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
