from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from books import views
from books.router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.books_list_view, name='list'),
    path('add/', views.books_add_view, name='add'),
    path('import/', views.books_import_view, name='import'),

    path('api/', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
