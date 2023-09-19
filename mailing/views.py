from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from mailing.forms import MailingForm, MessageForm
from mailing.models import Mailing, MailingLog, Message


class UserMailingsMixin:
    """Миксин для фильтрации рассылок по пользователю.
    Если пользователь менеджер - возвращаем все рассылки.
    Если обычный пользователь - то только его рассылки"""
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Mailing.objects.all()
        return Mailing.objects.filter(user=user)


class MailingListView(LoginRequiredMixin, UserPassesTestMixin, UserMailingsMixin, ListView):
    """Список рассылок для просмотра"""
    model = Mailing

    def test_func(self):
        """Открывает доступ менеджеру к списку рассылок"""
        return True


class MailingDetailView(UserMailingsMixin, DetailView):
    """Подробная информация о рассылке"""
    model = Mailing

    def get_context_data(self, **kwargs):
        """Добавляет информацию о логах рассылки в контекст"""
        context_data = super().get_context_data(**kwargs)
        context_data['mailing_logs'] = MailingLog.objects.filter(mailing=self.object)
        return context_data


class MailingCreateView(UserPassesTestMixin, UserMailingsMixin, CreateView):
    """Создание новой рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        """Запрещает менеджеру создавать рассылки"""
        return not self.request.user.is_staff

    def get_form_kwargs(self):
        """Добавляет аргумент user в конструктор формы, равный текущему пользователю"""
        kwargs = super().get_form_kwargs()
        user = self.request.user
        # Фильтруем клиентов, принадлежащих текущему пользователю
        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляет форму для создания сообщения в контекст"""
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm()
        return context

    def form_valid(self, form):
        """Обрабатывает форму создания рассылки и сообщения"""

        # Обработка формы сообщения
        message_form = MessageForm(self.request.POST)
        if message_form.is_valid():
            message = message_form.save()

            # Получаем пользователя
            user = self.request.user
            form.instance.user = user

            # Сохраняем рассылку
            mailing = form.save(commit=False)
            mailing.message = message
            mailing.save()

            # Получаем клиентов для рассылки
            selected_clients = form.cleaned_data['clients']
            mailing.clients.set(selected_clients)
            mailing.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class MailingUpdateView(UserPassesTestMixin, UpdateView):
    """Редактирование существующей рассылки"""
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'

    def test_func(self):
        """Запрещает менеджеру редактировать рассылки"""
        return not self.request.user.is_staff

    def get_success_url(self):
        """Получаем урл после успешного редактирования"""
        return reverse('mailing:view', args=[self.kwargs['pk']])

    def get_form_kwargs(self):
        """Добавляет аргумент user в конструктор формы, равный текущему пользователю"""
        kwargs = super().get_form_kwargs()
        user = self.request.user
        kwargs['user'] = user
        return kwargs

    def get_context_data(self, **kwargs):
        """Добавляет форму сообщения в контекст"""
        context = super().get_context_data(**kwargs)
        context['message_form'] = MessageForm(instance=self.object.message)
        return context

    def form_valid(self, form):
        message_form = MessageForm(self.request.POST, instance=self.object.message)
        if message_form.is_valid():
            message = message_form.save()

            form.instance.user = self.request.user
            form.instance.message = message
            form.save()

            selected_clients = form.cleaned_data['clients']
            form.instance.clients.set(selected_clients)
            form.save()

            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class MailingDeleteView(UserPassesTestMixin, DeleteView):
    """Удаляет рассылку"""
    model = Mailing
    success_url = reverse_lazy('mailing:list')

    def test_func(self):
        """Запрещает менеджеру удалять рассылки"""
        return not self.request.user.is_staff


def toggle_mailing_status(request, pk, action):
    """Активирует / отключает рассылку"""

    mailing = get_object_or_404(Mailing, pk=pk)

    if action == 'start':
        # Запуск рассылки
        mailing.status = Mailing.STATUS_STARTED
        mailing.save()
    elif action == 'stop':
        # Остановка рассылки
        mailing.status = Mailing.STATUS_DONE
        mailing.save()

    return HttpResponseRedirect(reverse('mailing:view', args=[pk]))


def mailing_report(request):
    """Отчет о рассылках"""

    user = request.user
    mailings = Mailing.objects.filter(user=user)
    context = {
        'mailings': mailings,
    }
    return render(request, 'mailing/mailing_report.html', context)


class MailingLogListView(ListView):
    """Просмотр логов рассылки"""

    model = MailingLog
    template_name = 'mailing/mailing_logs_list.html'
    context_object_name = 'mailing_logs'

    def get_queryset(self):
        """Фильтруем логи по рассылке"""
        queryset = super().get_queryset()
        queryset = queryset.filter(mailing_id=self.kwargs['pk'])
        return queryset

    def get_context_data(self, **kwargs):
        """Добавляем pk рассылки в контекст"""
        context = super().get_context_data(**kwargs)
        context['mailing_pk'] = self.kwargs['pk']
        return context
