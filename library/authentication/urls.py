from django.urls import path
from authentication import views

app_name = 'authentication'

urlpatterns = [
    path('', views.index_view, name='index_auth'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/update/<int:user_id>', views.update_profile, name='update_profile'),
    path('users/', views.list_of_users_view, name='list_of_users'),
    path('users/<int:user_id>', views.user_details_view, name='user_details')
]