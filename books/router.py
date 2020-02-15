from rest_framework.routers import DefaultRouter

from books.api.viewsets import AuthorViewSet, BookViewSet, LanguageViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet)
router.register(r'books', BookViewSet)
router.register(r'languages', LanguageViewSet)
