from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView

from mailing.forms import MailingForm
from mailing.models import Mailing, MailingLog, Message


class MailingListView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_logs'] = MailingLog.objects.filter(mailing=self.object)
        return context_data


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:list')

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.save()

        selected_clients = form.cleaned_data['clients']
        mailing.clients.set(selected_clients)

        return redirect(self.success_url)


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailing:list')


class MessageDetailView(DetailView):
    model = Message


def mailing_report(request):
    mailings = Mailing.objects.all()
    context = {
        'mailings': mailings,
    }
    return render(request, 'mailing/mailing_report.html', context)


class MailingLogListView(ListView):
    model = MailingLog
    template_name = 'mailing/mailing_logs_list.html'
    context_object_name = 'mailing_logs'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Mailing.objects.get(pk=self.kwargs['pk'])  # Получение объекта Mailing по параметру 'pk'
        return context
