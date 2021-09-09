from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AppPagesTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser')

    def test_main_page(self):
        url = reverse('main')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_pages/main.html')
