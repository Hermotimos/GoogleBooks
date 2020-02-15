from rest_framework.routers import DefaultRouter

from books.api.viewsets import AuthorViewSet, BookViewSet, LanguageViewSet

router = DefaultRouter()
router.register('authors', AuthorViewSet)
router.register('books', BookViewSet)
router.register('languages', LanguageViewSet)

for url in router.urls:
    print(url)
