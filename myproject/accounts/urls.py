"""
accounts/urls.py - URL маршруты для аутентификации
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Регистрация
    path('register/', views.register_view, name='register'),

    # Авторизация
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Профиль
    path('profile/', views.profile_view, name='profile'),
]