from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_of_books, name='list_of_books'),
    path('create/', views.create_a_book, name='create_a_book'),
    path('ordered/<int:user_id>/', views.ordered_books_by_user, name='ordered_books_by_user'),
    path('<int:book_id>/', views.book_detail, name='book_detail')
]