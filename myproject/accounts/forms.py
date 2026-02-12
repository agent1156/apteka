"""
accounts/forms.py - Формы для регистрации и входа
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User


class RegisterForm(UserCreationForm):
    """
    Форма для регистрации нового пользователя
    """

    # Кастомизация полей
    email = forms.EmailField(
        label='Email адрес *',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    password1 = forms.CharField(
        label='Пароль *',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        }),
        help_text='Минимум 8 символов'
    )

    password2 = forms.CharField(
        label='Подтверждение пароля *',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    )

    first_name = forms.CharField(
        label='Имя',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иван'
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует.')
        return email

    def save(self, commit=True):
        """Сохранение пользователя"""
        user = super().save(commit=False)
        user.username = user.email.split('@')[0]

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):
    """
    Форма для входа пользователя
    """

    email = forms.EmailField(
        label='Email *',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@email.com'
        })
    )

    password = forms.CharField(
        label='Пароль *',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

    remember_me = forms.BooleanField(
        label='Запомнить меня',
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )

    def clean(self):
        """Валидация формы"""
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # Аутентификация по email
            user = authenticate(email=email, password=password)
            if user is None:
                raise ValidationError('Неверный email или пароль.')
            if not user.is_active:
                raise ValidationError('Аккаунт не активен.')

            cleaned_data['user'] = user

        return cleaned_data