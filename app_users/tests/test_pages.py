from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsersPagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser')

    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/login.html')

    def test_account_page(self):
        self.client.force_login(User.objects.get(username='testuser'))
        url = reverse('account')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/account.html')

    def test_cart_page(self):
        self.client.force_login(User.objects.get(username='testuser'))
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_users/cart.html')
