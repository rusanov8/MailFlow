from django.conf import settings
from django.core.mail import send_mail


def send_email_for_verify(user, verify_link):
    """Отправляет сообщение для верификации"""

    subject = 'Подтверждение email на MailFlow'
    message = f'Пройдите по ссылке для подтверждения вашего email: {verify_link}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)


def send_block_email(user):
    """Отправляет сообщение о блокировке"""

    subject = 'MailFlow: Вы заблокированы'
    message = 'Ваша учетная запись заблокирована. Свяжитесь с нами для уточнения обстоятельств.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
