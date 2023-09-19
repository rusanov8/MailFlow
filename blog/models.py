from django.db import models

from users.models import User


class Blog(models.Model):
    """Модель для хранения информации о статьях блога"""

    title = models.CharField(max_length=255, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое')
    image = models.ImageField(upload_to='blog/', verbose_name='Изображение', null=True, blank=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        db_table = 'blog'
