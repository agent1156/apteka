# contact/models.py
from django.db import models


class Feedback(models.Model):
    """
    Модель для обратной связи
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Имя'
    )

    subject = models.CharField(
        max_length=200,
        verbose_name='Тема'
    )

    email = models.EmailField(
        max_length=254,
        verbose_name='Email'
    )

    message = models.TextField(
        verbose_name='Сообщение'
    )

    class Meta:
        verbose_name = 'Обратная связь'
        verbose_name_plural = 'Обратная связь'

    def __str__(self):
        return f'{self.name} - {self.subject}'