from django import forms
from .models import Feedback


class FeedbackForm(forms.ModelForm):
    """
    Форма обратной связи на основе модели Feedback
    """

    class Meta:
        model = Feedback
        fields = ['name', 'subject', 'email', 'message']

        # Виджеты для стилизации полей
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Введите ваше имя',
                'autofocus': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Вопрос по услугам'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'example@mail.com'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Напишите ваше сообщение здесь...'
            }),
        }

        # Метки полей (labels)
        labels = {
            'name': 'Ваше имя',
            'subject': 'Тема обращения',
            'email': 'Электронная почта',
            'message': 'Сообщение',
        }

        # Сообщения об ошибках
        error_messages = {
            'name': {
                'required': 'Пожалуйста, укажите ваше имя',
                'max_length': 'Имя не может быть длиннее 100 символов',
            },
            'subject': {
                'required': 'Укажите тему обращения',
                'max_length': 'Тема не может быть длиннее 200 символов',
            },
            'email': {
                'required': 'Email обязателен для обратной связи',
                'invalid': 'Введите корректный email адрес',
            },
            'message': {
                'required': 'Напишите текст сообщения',
            },
        }

    def clean_name(self):
        """Валидация имени"""
        name = self.cleaned_data.get('name')
        if len(name) < 5:
            raise forms.ValidationError('Имя должно содержать минимум 5 символа')
        return   name.strip().title()

    def clean_message(self):
        """Валидация сообщения"""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Сообщение должно содержать минимум 10 символов')
        return message.strip()

    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get('email')
        return email.lower()