from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    Модель категории новостей
    """
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL-адрес')
    description = models.TextField(verbose_name='Описание', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class News(models.Model):
    """
    Модель новости
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (DRAFT, 'Черновик'),
        (PUBLISHED, 'Опубликовано'),
        (ARCHIVED, 'В архиве'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL-адрес')
    content = models.TextField(verbose_name='Содержание')
    short_description = models.TextField(max_length=500, verbose_name='Краткое описание', blank=True)

    # Связь с категорией
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Категория'
    )

    # Связь с автором
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='news',
        verbose_name='Автор'
    )

    # Статус новости
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        verbose_name='Статус'
    )

    # Даты
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата публикации')

    # Изображение
    image = models.ImageField(
        upload_to='news/images/%Y/%m/%d/',
        verbose_name='Изображение',
        blank=True,
        null=True
    )

    # Счетчик просмотров
    views = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров')

    # Теги
    tags = models.CharField(max_length=200, verbose_name='Теги', blank=True)

    # Мета-информация для SEO
    meta_title = models.CharField(max_length=200, verbose_name='Meta заголовок', blank=True)
    meta_description = models.TextField(verbose_name='Meta описание', blank=True)

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Автоматически устанавливаем дату публикации при изменении статуса на "опубликовано"
        if self.status == self.PUBLISHED and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        elif self.status != self.PUBLISHED:
            self.published_at = None
        super().save(*args, **kwargs)


class NewsComment(models.Model):
    """
    Модель комментария к новости
    """
    news = models.ForeignKey(
        News,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Новость'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    content = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f'Комментарий от {self.user.username} к "{self.news.title}"'