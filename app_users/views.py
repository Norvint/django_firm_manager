from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView, ListView

from app_organizations.models import Worker
from app_storage.models import Cart, CartProduct


class CustomLoginView(LoginView):
    template_name = 'app_users/login.html'


class CustomLogoutView(LogoutView):
    pass


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/account.html'

    def get_context_data(self, **kwargs):
        context = super(UserAccountView, self).get_context_data(**kwargs)
        try:
            worker = Worker.objects.get(user=self.request.user)
            context['worker'] = worker
        except ObjectDoesNotExist:
            context['worker'] = None
        return context


class CartView(ListView):
    template_name = 'app_users/cart.html'
    context_object_name = 'products_in_cart'

    def get_queryset(self):
        cart = Cart.objects.get(user=self.request.user)
        queryset = CartProduct.objects.filter(cart=cart)
        return queryset