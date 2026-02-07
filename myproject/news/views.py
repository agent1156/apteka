from django.shortcuts import render

def index(request):
    """Главная страница приложения news"""
    context = {
        'title': 'Новостной портал',
        'message': 'Добро пожаловать!',
        'current_time': '19:30'
    }
    return render(request, 'news/index.html', context)