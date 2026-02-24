from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from .models import Feedback
from .forms import FeedbackForm


def feedback_create(request):
    """
    Представление для создания нового обращения
    """
    if request.method == 'POST':
        # Обработка отправленной формы
        form = FeedbackForm(request.POST)
        if form.is_valid():
            # Сохраняем данные в базу
            feedback = form.save()

            # Добавляем сообщение об успехе
            messages.success(
                request,
                'Спасибо за обращение! Мы свяжемся с вами в ближайшее время.'
            )

            # Перенаправляем на страницу успеха
            return redirect('contact:success')
        else:
            # Если форма невалидна, показываем ошибку
            messages.error(
                request,
                'Пожалуйста, исправьте ошибки в форме.'
            )
    else:
        # GET запрос - показываем пустую форму
        form = FeedbackForm()

    return render(request, 'contact/feedback_form.html', {
        'form': form,
        'title': 'Обратная связь',
        'button_text': 'Отправить сообщение'
    })


def feedback_success(request):
    """
    Представление для страницы успешной отправки
    """
    return render(request, 'contact/feedback_success.html', {
        'title': 'Сообщение отправлено'
    })


def feedback_list(request):
    """
    Представление для списка всех обращений (только для админов)
    """
    # Получаем все обращения, сортируем по дате (новые сверху)
    feedbacks = Feedback.objects.all()

    # Пагинация - 10 элементов на страницу
    paginator = Paginator(feedbacks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'contact/feedback_list.html', {
        'page_obj': page_obj,
        'title': 'Список обращений'
    })


def feedback_detail(request, pk):
    """
    Представление для детального просмотра обращения (только для админов)
    """
    feedback = get_object_or_404(Feedback, pk=pk)

    return render(request, 'contact/feedback_detail.html', {
        'feedback': feedback,
        'title': f'Обращение #{feedback.id}'
    })