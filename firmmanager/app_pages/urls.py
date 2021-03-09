from django.urls import path

from app_pages.views import MainPageView


urlpatterns = [
    path('', MainPageView.as_view(), name='main')
]
