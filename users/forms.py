from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from users.models import User


class FormStyleMixin:
    """Миксин для стилизации форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = f'{field.label}'
            field.label = ''
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(FormStyleMixin, UserCreationForm):
    """Форма для регистрации клиента"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''


class UserProfileForm(FormStyleMixin, UserChangeForm):
    """Форма для редактирования профиля клиента"""

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.HiddenInput()
