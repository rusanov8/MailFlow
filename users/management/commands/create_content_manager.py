from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    """Создает контент-менеджера"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email='content_manager_1@mailflow.ru',
            first_name='Петр',
            last_name='Петров',
            is_staff=True,
        )

        user.set_password('mailflow88')
        user.save()
