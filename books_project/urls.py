from django.contrib import admin
from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from books import views
from books.router import router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.books_list_view, name='list'),
    path('add/', views.books_add_view, name='add'),

    path('api/', include(router.urls))
]

# urlpatterns = format_suffix_patterns(urlpatterns)
