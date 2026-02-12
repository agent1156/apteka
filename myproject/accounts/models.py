# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# УДАЛИТЕ ВСЮ КАСТОМНУЮ МОДЕЛЬ User!
# class User(AbstractUser):
#     email = models.EmailField(...)
#     ...

# Вместо этого создайте ТОЛЬКО профиль:
class Profile(models.Model):
    """Профиль пользователя для расширения стандартной модели"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True,
        null=True
    )
    bio = models.TextField(
        'О себе',
        max_length=500,
        blank=True
    )
    avatar = models.ImageField(
        'Аватар',
        upload_to='avatars/',
        blank=True,
        null=True
    )
    email_verified = models.BooleanField(
        'Email подтвержден',
        default=False
    )
    
    def __str__(self):
        return f'Профиль {self.user.username}'
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


# Сигналы для автоматического создания профиля
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создать профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранить профиль"""
    if hasattr(instance, 'profile'):
        instance.profile.save()