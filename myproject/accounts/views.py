"""
accounts/views.py - Обработчики запросов
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from .models import User


def register_view(request):
    """
    Регистрация нового пользователя
    """
    # Если пользователь уже авторизован, перенаправляем в профиль
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Создаем пользователя
            user = form.save()

            # Автоматически авторизуем пользователя
            login(request, user)

            # Сообщение об успехе
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')

            # Перенаправляем в профиль
            return redirect('accounts:profile')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Вход пользователя в систему
    """
    # Если пользователь уже авторизован, перенаправляем в профиль
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Получаем пользователя из очищенных данных
            user = form.cleaned_data['user']

            # Авторизуем пользователя
            login(request, user)

            # Настройка сессии для "Запомнить меня"
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)  # Сессия до закрытия браузера

            # Приветственное сообщение
            welcome_name = user.get_full_name() or user.email
            messages.success(request, f'Добро пожаловать, {welcome_name}!')

            # Перенаправляем на следующую страницу или в профиль
            next_url = request.GET.get('next', 'accounts:profile')
            return redirect(next_url)
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    Выход пользователя из системы
    """
    logout(request)
    messages.success(request, 'Вы успешно вышли из системы.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """
    Страница профиля пользователя
    """
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })