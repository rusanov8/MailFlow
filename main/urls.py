from django.urls import path

from main.apps import MainConfig
from main.views import home, contacts

app_name = MainConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contacts/', contacts, name='contacts'),
]
