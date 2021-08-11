from django.urls import path

from app_users.views import CustomLoginView, CustomLogoutView, UserAccountView, CartView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account/', UserAccountView.as_view(), name='account'),
    path('cart/', CartView.as_view(), name='cart'),
]
