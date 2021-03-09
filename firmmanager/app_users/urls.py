from django.urls import path

from app_users.views import CustomLoginView, CustomLogoutView, UserAccountView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('account/', UserAccountView.as_view(), name='account'),
]
