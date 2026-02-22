from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    """Модель категории товаров"""

    name = models.CharField(
        max_length=200,
        verbose_name="Название категории"
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL-идентификатор"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='children',
        blank=True,
        null=True,
        verbose_name="Родительская категория"
    )
    description = models.TextField(
        verbose_name="Описание",
        blank=True
    )
    image = models.ImageField(
        upload_to='categories/',
        verbose_name="Изображение",
        blank=True,
        null=True
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активна"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )

    # SEO
    meta_title = models.CharField(
        max_length=255,
        verbose_name="Meta Title",
        blank=True
    )
    meta_description = models.TextField(
        verbose_name="Meta Description",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Категория товаров"
        verbose_name_plural = "Категории товаров"
        ordering = ['sort_order', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """Расширенная модель товара с категориями"""

    # Связи
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Категория"
    )

    # Основные поля
    name = models.CharField(
        max_length=255,
        verbose_name="Название товара"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name="URL-идентификатор"
    )
    article = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Артикул",
        db_index=True
    )
    barcode = models.CharField(
        max_length=100,
        verbose_name="Штрих-код",
        blank=True
    )

    # Цены
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена"
    )
    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Закупочная цена",
        blank=True,
        null=True
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена со скидкой",
        blank=True,
        null=True
    )

    # Характеристики
    brand = models.CharField(
        max_length=200,
        verbose_name="Бренд",
        blank=True
    )
    weight = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name="Вес (кг)",
        blank=True,
        null=True
    )
    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество на складе"
    )

    # Контент
    description = models.TextField(
        verbose_name="Полное описание",
        blank=True
    )
    specifications = models.JSONField(
        verbose_name="Характеристики",
        default=dict,
        blank=True,
        help_text="Характеристики товара в формате JSON"
    )

    # Медиа
    main_image = models.ImageField(
        upload_to='products/main/',
        verbose_name="Главное изображение",
        blank=True,
        null=True
    )

    # Статусы
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
        db_index=True
    )
    is_hit = models.BooleanField(
        default=False,
        verbose_name="Хит продаж"
    )
    is_new = models.BooleanField(
        default=False,
        verbose_name="Новинка"
    )
    is_recommended = models.BooleanField(
        default=False,
        verbose_name="Рекомендуемый"
    )

    # Статистика
    views_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество просмотров"
    )
    purchases_count = models.PositiveIntegerField(
        default=0,
        verbose_name="Количество покупок"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0,
        verbose_name="Рейтинг"
    )

    # Даты
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )
    published_at = models.DateTimeField(
        verbose_name="Дата публикации",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug', 'is_active']),
            models.Index(fields=['article']),
            models.Index(fields=['category', 'is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.article})"

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={
            'category_slug': self.category.slug,
            'product_slug': self.slug
        })

    @property
    def current_price(self):
        """Возвращает актуальную цену со скидкой"""
        return self.discount_price if self.discount_price else self.price

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Дополнительные изображения товара"""

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Товар"
    )
    image = models.ImageField(
        upload_to='products/extra/',
        verbose_name="Изображение"
    )
    alt_text = models.CharField(
        max_length=255,
        verbose_name="Alt текст",
        blank=True
    )
    is_main = models.BooleanField(
        default=False,
        verbose_name="Главное изображение"
    )
    sort_order = models.PositiveIntegerField(
        default=0,
        verbose_name="Порядок сортировки"
    )

    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"
        ordering = ['sort_order']

    def __str__(self):
        return f"Изображение для {self.product.name}"