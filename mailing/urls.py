from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingDeleteView, MessageDetailView, mailing_report, MailingLogListView

app_name = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('view/<int:pk>/', MailingDetailView.as_view(), name='view'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),
    path('report/', mailing_report, name='report'),
    path('<int:pk>/logs/', MailingLogListView.as_view(), name='mailing_logs')
    ]
