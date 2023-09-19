from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from clients.forms import ClientForm
from clients.models import Client


class UserClientsMixin:
    """Миксин для получения из списка клиентов только клиентов текущего пользователя"""
    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)


class ClientCreateView(LoginRequiredMixin, UserClientsMixin, CreateView):
    """Контроллер для создания нового клиента"""
    model = Client
    form_class = ClientForm

    success_url = reverse_lazy('clients:list')

    def form_valid(self, form):
        user = self.request.user  # Получаем текущего пользователя
        form.instance.user = user  # Привязываем клиента к текущему пользователю
        return super().form_valid(form)


class ClientListView(LoginRequiredMixin, UserClientsMixin, ListView):
    """Контроллер для отображения списка клиентов"""
    model = Client


class ClientDetailView(UserClientsMixin, DetailView):
    """Контроллер для отображения информации о клиенте"""
    model = Client


class ClientUpdateView(UserClientsMixin, UpdateView):
    """Контроллер для изменения информации о клиенте"""
    model = Client
    form_class = ClientForm

    def get_success_url(self):
        return reverse('clients:view', args=[self.kwargs.get('pk')])


class ClientDeleteView(UserClientsMixin, DeleteView):
    """Контроллер для удаления клиента"""
    model = Client
    success_url = reverse_lazy('clients:list')

