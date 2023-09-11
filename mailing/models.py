from django.db import models
from clients.models import Client


class Message(models.Model):
    """Модель для хранения информации о сообщениях для рассылки"""

    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        db_table = 'messages'


class Mailing(models.Model):
    """Модель для хранения информации о рассылках"""

    PERIOD_DAILY = 'daily'
    PERIOD_WEEKLY = 'weekly'
    PERIOD_MONTHLY = 'monthly'

    PERIODS = (
        (PERIOD_DAILY, 'Ежедневная'),
        (PERIOD_WEEKLY, 'Раз в неделю'),
        (PERIOD_MONTHLY, 'Раз в месяц')
    )

    STATUS_CREATED = 'created'
    STATUS_STARTED = 'started'
    STATUS_DONE = 'done'

    STATUSES = (
        (STATUS_CREATED, 'Создана'),
        (STATUS_STARTED, 'Запущена'),
        (STATUS_DONE, 'Завершена')
    )

    send_time = models.TimeField(verbose_name='Время старта рассылки')
    end_time = models.DateTimeField(verbose_name='Время окончания рассылки', null=True, blank=True)
    frequency = models.CharField(max_length=20, choices=PERIODS, verbose_name='Периодичность')
    status = models.CharField(max_length=20, choices=STATUSES,
                              verbose_name='Статус рассылки', default='Создана')

    # Связь с клиентами (ManyToMany)
    clients = models.ManyToManyField(Client, verbose_name='Клиенты')

    # Связь с сообщением (ForeignKey)
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')

    def __str__(self):
        return f'Рассылка от {self.send_time}'

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        db_table = 'mailings'


class MailingLog(models.Model):
    """Модель для хранения логов рассылок"""
    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    STATUSES = (
        (STATUS_OK, 'Успешно'),
        (STATUS_FAILED, 'Ошибка')

    )

    last_try = models.DateTimeField(verbose_name='Дата и время последней попытки', auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUSES, verbose_name='Статус попытки')
    response = models.TextField(verbose_name='Ответ почтового сервера', null=True, blank=True)

    # Связь с рассылкой (ForeignKey)
    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='Рассылка')

    def __str__(self):
        return f'Рассылка от {self.last_try}. Статус: {self.status}'

    class Meta:
        verbose_name = 'Лог рассылки'
        verbose_name_plural = 'Логи рассылок'
        db_table = 'mailing_logs'

