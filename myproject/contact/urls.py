from django.urls import path
from . import views

# Пространство имен для приложения
app_name = 'contact'

urlpatterns = [
    # Главная страница обратной связи (форма)
    path('', views.feedback_create, name='feedback'),

    # Страница успешной отправки
    path('success/', views.feedback_success, name='success'),

    # Список всех обращений (для администраторов)
    path('list/', views.feedback_list, name='list'),

    # Детальный просмотр обращения (для администраторов)
    path('detail/<int:pk>/', views.feedback_detail, name='detail'),

    # Альтернативные URL для удобства
    path('create/', views.feedback_create, name='create'),  # синоним для feedback
    path('send/', views.feedback_create, name='send'),  # еще один синоним
]