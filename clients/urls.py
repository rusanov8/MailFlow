from django.urls import path

from clients.apps import ClientsConfig
from clients.views import ClientCreateView, ClientListView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='list'),  # теперь передаем класс, и вызываем функцию as_view()
    path('view/<int:pk>/', ClientDetailView.as_view(), name='view'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
    ]
