from django.core.management import BaseCommand
from mailing.services import send_mailing
from mailing.models import Mailing


class Command(BaseCommand):
    help = 'Отправить рассылку'

    def add_arguments(self, parser):
        parser.add_argument('mailing_id', type=int, help='ID рассылки для отправки')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        try:
            mailing = Mailing.objects.get(pk=mailing_id)
        except Mailing.DoesNotExist:
            self.stdout.write(self.style.ERROR('Рассылка с указанным ID не найдена.'))
            return

        mailing.status = 'started'
        mailing.save()
        self.stdout.write(self.style.SUCCESS(f'Отправка рассылки "{mailing.message.subject}" начата...'))

        try:
            send_mailing(mailing_id)
            mailing.status = 'completed'
            mailing.save()
            self.stdout.write(self.style.SUCCESS(f'Рассылка сообщения "{mailing.message.subject}" успешно отправлена'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при отправке рассылки: {str(e)}'))





