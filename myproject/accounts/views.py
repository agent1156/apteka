"""
accounts/views.py - Обработчики запросов
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth.models import User
from django import forms

def home(request):
    context = {
        'posts': 'Посты',
        'title': 'Мои посты'
    }
    return render(request,'accounts/home.html',context)
def register_view(request):
    """
    Регистрация нового пользователя
    """
    if request.user.is_authenticated:
        return redirect('accounts:profile')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна! Добро пожаловать!')
            return redirect('accounts:profile')
    else:
        form = UserRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    Вход пользователя в систему
    """
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)

            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)

            welcome_name = user.get_full_name() or user.email
            messages.success(request, f'Добро пожаловать, {welcome_name}!')

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


@login_required
def profile_edit_view(request):
    """
    Редактирование профиля пользователя
    """
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('accounts:profile')
    else:
        form = UserEditForm(instance=request.user)

    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def change_password_view(request):
    """
    Смена пароля пользователя
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен!')
            return redirect('accounts:profile')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'accounts/change_password.html', {'form': form})


class UserEditForm(forms.ModelForm):
    """Форма для редактирования данных пользователя"""

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Электронная почта',
        }
        help_texts = {
            'username': 'Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_',
        }