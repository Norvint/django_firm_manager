from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView


class CustomLoginView(LoginView):
    template_name = 'app_users/login.html'


class CustomLogoutView(LogoutView):
    pass


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/account.html'
