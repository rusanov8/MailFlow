from django.conf import settings
from django.core.cache import cache
from blog.models import Blog


def get_cached_articles():
    """Кжширует статьи блога"""

    if settings.CACHE_ENABLED:
        key = 'articles'
        articles = cache.get(key)
        if articles is None:
            articles = Blog.objects.all()
            cache.set(key, articles)

    else:
        articles = Blog.objects.all()

    return articles
