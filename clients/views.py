from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from clients.models import Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('full_name', 'email', 'comment', )

    success_url = reverse_lazy('clients:list')


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('full_name', 'email', 'comment',)

    def get_success_url(self):
        return reverse('clients:view', args=[self.kwargs.get('pk')])


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('clients:list')

