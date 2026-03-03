from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class MenuItem(models.Model):
    MENU_TYPES = (
        ('catalog','Каталог'),
        ('subcatalog','Подкаталог'),
        ('news','Новости'),
        ('url', 'Внедняя ссылка')
    )
    title = models.CharField('Название', max_length=100)
    slug = models.SlugField('URL', max_length=100,blank=True)








