from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.views import RegisterView, ProfileView, verify_email, UserListView, UserDetailView, toggle_activity
from users.apps import UsersConfig

app_name = UsersConfig.name
urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView .as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView .as_view(), name='profile'),
    path('verify_email/<str:key>/', verify_email, name='verify_email'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('view/<int:pk>/', UserDetailView.as_view(), name='view'),
    path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity'),

    ]
