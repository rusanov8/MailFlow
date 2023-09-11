from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from mailing.models import Mailing, MailingLog
import datetime


def send_mailing(mailing_id):
    try:
        mailing = Mailing.objects.get(pk=mailing_id)

        result = send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email='rusanov.egor@bk.ru',
            recipient_list=[client.email for client in mailing.clients.all()],
            fail_silently=False
        )

        MailingLog.objects.create(
            status=MailingLog.STATUS_OK if result else MailingLog.STATUS_FAILED,
            response=result,
            mailing=mailing
        )

    except ObjectDoesNotExist:
        # Обработка ошибки, если рассылка с заданным mailing_id не найдена
        print("Рассылка с указанным ID не найдена.")
        return


def schedule_mailing():

    now = datetime.datetime.now()
    for mailing in Mailing.objects.filter(status=Mailing.STATUS_STARTED):  # берем все рассылки со статусом 'запущена'
        if (now > mailing.send_time) and (now < mailing.end_time):

            mailing_log =  MailingLog.objects.filter(mailing=mailing)

            if mailing_log.exists():
                last_try_date = mailing_log.order_by('send_time').first().send_time

                if mailing.frequency == Mailing.PERIOD_DAILY:
                    if (now - last_try_date).days >= 1:
                        send_mailing(mailing_id=mailing.id)
                elif mailing.frequency == Mailing.PERIOD_WEEKLY:
                    if (now - last_try_date).days >= 70:
                        send_mailing(mailing_id=mailing.id)
                if mailing.frequency == Mailing.PERIOD_MONTHLY:
                    if (now - last_try_date).days >= 30:
                        send_mailing(mailing_id=mailing.id)

            else:
                send_mailing(mailing_id=mailing.id)







