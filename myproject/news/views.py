

# news/views.py
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from .models import News


def index(request):
    """Главная страница со списком новостей"""
    news = News.objects.filter(status='published').order_by('-created_at')
    context = {
        'title': 'Новостной портал',
        'message': 'Добро пожаловать!',
        'news': news,
    }
    return render(request, 'news/index.html', context)


def news_detail(request, news_id):
    """
    Детальная страница новости
    :param request: HTTP запрос
    :param news_id: ID новости
    :return: Детальная страница новости
    """
    try:
        # Получаем новость или возвращаем 404
        news_item = get_object_or_404(News, id=news_id, status='published')

        # Увеличиваем счетчик просмотров
        news_item.views += 1
        news_item.save(update_fields=['views'])

        # Получаем похожие новости (из той же категории)
        related_news = News.objects.filter(
            category=news_item.category,
            status='published'
        ).exclude(id=news_id).order_by('-created_at')[:3]

        context = {
            'news': news_item,
            'title': news_item.title,
            'related_news': related_news,
        }

        return render(request, 'news/news_detail.html', context)

    except News.DoesNotExist:
        raise Http404("Новость не найдена")