from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_of_orders, name='list_of_orders'),
    path('create/', views.create_an_order, name='create_an_order'),
    path('<int:user_id>/', views.user_orders, name='user_orders'),
    path('close/<int:order_id>/', views.close_an_order, name='close_an_order')
]