from django import forms

from clients.models import Client


class ClientForm(forms.ModelForm):
    """Форма для работы с клиентом"""

    class Meta:
        model = Client
        fields = ('email', 'full_name', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'