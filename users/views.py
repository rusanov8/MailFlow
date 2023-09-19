import secrets

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, ListView, DetailView

from mailing.models import Mailing
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from users.services import send_email_for_verify, send_block_email


# Create your views here.
class RegisterView(CreateView):
    """регистрация пользователя"""

    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        if form.is_valid():
            verify_key = secrets.token_urlsafe(32)

            user = form.save(commit=False)
            user.verify_key = verify_key
            user.save()

            current_site = get_current_site(self.request)
            verify_link = f"http://{current_site.domain}{reverse('users:verify_email', args=[verify_key])}"
            send_email_for_verify(user, verify_link)
            return render(self.request, 'users/verification/verify_email.html')

        return super().form_valid(form)


class ProfileView(UpdateView):
    """Отображение профиля пользователя"""

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('main:home')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, key):
    """Верификация по почте"""

    user = User.objects.filter(verify_key=key).first()

    if user:
        user.is_verified = True
        user.save()
        return render(request, 'users/verification/verify_success.html')
    else:
        return render(request, 'users/verification/verify_error.html')


class UserListView(UserPassesTestMixin, ListView):
    """Просмотр списка пользователей"""
    model = User

    def test_func(self):
        return self.request.user.is_staff


class UserDetailView(DetailView):
    """Просмотр информации о пользователе"""
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.object
        mailings_count = len(Mailing.objects.filter(user=user))
        active_mailings_count = len(Mailing.objects.filter(user=user, status='started'))
        context['mailings_count'] = mailings_count
        context['active_mailings_count'] = active_mailings_count
        return context


@user_passes_test(lambda u: u.is_staff)
def toggle_activity(request, pk):
    """Активирует / деактивирует пользователя"""

    user_item = get_object_or_404(User, pk=pk)
    if user_item.is_active:
        user_item.is_active = False
        send_block_email(user_item)
    else:
        user_item.is_active = True

    user_item.save()

    return redirect(reverse('users:view', kwargs={'pk': pk}))
