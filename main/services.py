from django.conf import settings
from django.core.cache import cache

from clients.models import Client
from mailing.models import Mailing


def get_cached_unique_clients():
    """Кэширует клиентов"""
    if settings.CACHE_ENABLED:
        key = 'unique_clients'
        unique_clients = cache.get(key)
        if unique_clients is None:
            unique_clients = Client.objects.values_list('email', flat=True).distinct()
            cache.set(key, unique_clients)

    else:
        unique_clients = Client.objects.values_list('email', flat=True).distinct()

    return unique_clients


def get_cached_mailings():
    """Кэширует рассылки"""
    if settings.CACHE_ENABLED:
        key = 'mailings'
        mailings = cache.get(key)
        if mailings is None:
            mailings = Mailing.objects.all()
            cache.set(key, mailings)

    else:
        mailings = Mailing.objects.all()
    return mailings


def get_active_mailings():
    """Получает активные рассылки из кэша"""
    cached_mailings = get_cached_mailings()
    if cached_mailings is not None:
        # Фильтруем рассылки по статусу "started" (или другому активному статусу)
        active_mailings = [mailing for mailing in cached_mailings if mailing.status == 'started']
        return active_mailings

    return None








