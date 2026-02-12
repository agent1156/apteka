# accounts/signals.py
from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import User


@receiver(post_migrate)
def create_permissions(sender, **kwargs):
    """Создание разрешений после миграции"""
    if sender.name == 'accounts':
        # Создаем ContentType для модели User
        content_type = ContentType.objects.get_for_model(User)

        # Создаем стандартные разрешения
        permissions = [
            ('add_user', 'Can add user'),
            ('change_user', 'Can change user'),
            ('delete_user', 'Can delete user'),
            ('view_user', 'Can view user'),
        ]

        for codename, name in permissions:
            Permission.objects.get_or_create(
                codename=codename,
                content_type=content_type,
                defaults={'name': name}
            )