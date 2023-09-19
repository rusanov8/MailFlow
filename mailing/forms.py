from django import forms
from mailing.models import Mailing, Message
from clients.models import Client


class FormStyleMixin:
    """Класс для стилизации форм"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class MailingForm(FormStyleMixin, forms.ModelForm):
    """Форма для создания и редактирования рассылок"""

    def __init__(self, *args, **kwargs):
        """Извлекает аргумент user из kwargs, который был передан в контроллере
        И в поле 'clients' формирует список из клиентов, принадлежащих этому пользователю"""
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['clients'].queryset = Client.objects.filter(user=user)

    send_time = forms.TimeField(
        label='Время рассылки',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    class Meta:
        model = Mailing
        fields = ('send_time', 'frequency', 'clients')


class MessageForm(FormStyleMixin, forms.ModelForm):
    """Форма для создания и редактирования сообщения"""
    class Meta:
        model = Message
        fields = ('subject', 'body')
