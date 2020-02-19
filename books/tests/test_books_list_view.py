from django.test import TestCase
from django.urls import resolve, reverse

from books import views
from books.filters import BookFilter
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
            pub_date='2000-01-01',
            pages=200,
            isbn='9780575079212',
            cover_url='https://www.abebooks.com/book-search/author/'
                      'PHILIP-K-DICK?cm_sp=brcr-_-bdp-_-author',
            language=cls.language_1
        )
        cls.book_2 = Book.objects.create(
            title='Title test 2',
            pub_date='1999-01-01',
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
        
        def check_filtering(test_case, obj, included_qs, excluded_qs, filter):
            test_case.assertTrue(obj in included_qs)
            for o in excluded_qs:
                self.assertTrue(o not in included_qs)
                print(f'Check filter "{filter}": "{o}" not in {included_qs}')
        
        for book in books:
            
            # Test filter by title
            in_title = book.title[:-1]
            f = BookFilter(data={'title': in_title}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(title__icontains=in_title)
            check_filtering(self, book, in_qs, out_qs, filter='title')
            
            # Test filter by language
            language_id = book.language.id
            f = BookFilter(data={'language': [language_id]}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(language_id=language_id)
            check_filtering(self, book, in_qs, out_qs, filter='language')

            # Test filter by author
            author_id = book.authors.first().id
            f = BookFilter(data={'authors': [author_id]}, queryset=books)
            in_qs = f.qs
            out_qs = Book.objects.exclude(authors__in=
                                          [a for a in book.authors.all()])
            check_filtering(self, book, in_qs, out_qs, filter='author')

        # Test filter by pub_date
        gt = '1998-12-31'
        lte = '1999-12-31'
        f = BookFilter(data={'pub_date_range_after': gt,
                             'pub_date_range_before': lte},
                       queryset=books)
        in_qs = f.qs
        out_qs = Book.objects.exclude(pub_date__gt=gt, pub_date__lte=lte)
        check_filtering(self, book, in_qs, out_qs, filter='pub_date')
