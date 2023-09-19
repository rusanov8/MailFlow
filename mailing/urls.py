from django.urls import path

from mailing.apps import MailingConfig
from mailing.views import MailingListView, MailingDetailView, MailingCreateView, MailingDeleteView,\
    mailing_report, MailingLogListView, toggle_mailing_status, MailingUpdateView

app_name = MailingConfig.name


urlpatterns = [
    path('', MailingListView.as_view(), name='list'),
    path('view/<int:pk>/', MailingDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', MailingUpdateView.as_view(), name='edit_mailing'),
    path('create/', MailingCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', MailingDeleteView.as_view(), name='delete'),
    path('report/', mailing_report, name='report'),
    path('<int:pk>/logs/', MailingLogListView.as_view(), name='mailing_logs'),
    path('toggle/<int:pk>/<str:action>/', toggle_mailing_status, name='toggle_mailing_status')
    ]
