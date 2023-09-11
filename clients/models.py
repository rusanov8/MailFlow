from django.db import models


class Client(models.Model):
    """Модель для хранения информации о клиентах сервиса"""

    email = models.EmailField(verbose_name='Контактный email')
    full_name = models.CharField(max_length=100, verbose_name='ФИО')
    comment = models.TextField(verbose_name='Комментарий', null=True, blank=True)

    def __str__(self):
        return f'{self.full_name} - {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        db_table = 'clients'

