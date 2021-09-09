from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UsersViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser', password='testpass')

    def test_login_view(self):
        url = reverse('login')
        response = self.client.post(url, data={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)
        new_response = self.client.get(reverse('account'))
        self.assertNotEqual(new_response.status_code, 302)

    def test_logout_view(self):
        self.client.force_login(User.objects.get(username='testuser'))
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        new_response = self.client.get(reverse('account'))
        self.assertNotEqual(new_response.status_code, 200)
