from django.urls import path
from books import views


app_name = 'books'
urlpatterns = [
    path('list', views.books_list_view, name='list'),
    path('add', views.books_add_view, name='add')
]
