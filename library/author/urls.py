from django.urls import path
from author import views

app_name = 'author'

urlpatterns = [
    path('', views.list_of_authors, name='list_of_authors'),
    path('create/', views.create_an_author, name='create_an_author'),
    path('<int:author_id>/', views.author_detail, name='author_detail'),
    path('update/<int:author_id>/', views.update_an_author, name='update_an_author'),
    path('delete/<int:author_id>/', views.delete_an_author, name='delete_an_author')
]