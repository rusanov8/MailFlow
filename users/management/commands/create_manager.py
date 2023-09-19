from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создает менеджера"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='manager_1@mailflow.ru',
            first_name='Иван',
            last_name='Иванов',
            is_staff=True,
        )

        user.set_password('mailflow88')
        user.save()
