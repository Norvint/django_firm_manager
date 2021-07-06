from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView

from app_organizations.models import Worker


class CustomLoginView(LoginView):
    template_name = 'app_users/login.html'


class CustomLogoutView(LogoutView):
    pass


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/account.html'

    def get_context_data(self, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        try:
            worker = Worker.objects.get(user=kwargs.get('pk'))
            context['worker'] = worker
        except ObjectDoesNotExist:
            context['worker'] = None
        return context
