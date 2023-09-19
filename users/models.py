from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """Модель пользователя"""

    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)

    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='Аватар', **NULLABLE)

    # Верификация
    verify_key = models.CharField(max_length=255, **NULLABLE, verbose_name='Ключ верификации')
    is_verified = models.BooleanField(default=False, verbose_name='Верифицирован')

    # Переопределяем поле для аутентификации
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        db_table = 'users'



