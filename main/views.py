from blog.services import get_cached_articles
from main.services import get_cached_unique_clients, \
    get_cached_mailings, get_active_mailings


from django.shortcuts import render


def home(request):
    """Отображение домашней страницы"""

    # Получаем данные для статистики из кэша
    total_mailings_count = len(get_cached_mailings())
    active_mailings_count = len(get_active_mailings())
    unique_clients_count = len(get_cached_unique_clients())
    articles = get_cached_articles().order_by('?')[:3]

    context = {
        'articles': articles,
        'total_mailings_count': total_mailings_count,
        'active_mailings_count': active_mailings_count,
        'unique_clients_count': unique_clients_count,
        'is_home_page': True,

    }
    return render(request, 'main/home.html', context)


def contacts(request):
    """Отображение страницы с контактами"""

    context = {
        'email': 'example@example.com',
        'phone': '+1 123-456-7890',
        'address': '123 Main Street, City, Country',
        'facebook': 'facebook.com/mailflow',
        'twitter': 'twitter.com/mailflow',
        'instagram': 'instagram.com/mailflow',

    }
    return render(request, 'main/contacts.html', context)

