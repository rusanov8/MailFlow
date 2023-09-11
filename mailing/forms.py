from django import forms
from mailing.models import Mailing
from clients.models import Client


class MailingForm(forms.ModelForm):
    send_time = forms.TimeField(
        label='Время рассылки',
        widget=forms.TimeInput(attrs={'type': 'time'}),
    )

    clients = forms.ModelMultipleChoiceField(
        label='Клиенты',
        queryset=Client.objects.all(),
        widget=forms.CheckboxSelectMultiple,)

    class Meta:
        model = Mailing
        fields = ['send_time', 'frequency', 'message', 'clients']