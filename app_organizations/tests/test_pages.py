import factory
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_organizations.models import Organization, Worker
from app_organizations.tests.factories import OrganizationFactory, WorkerFactory


class OrganizationPagesTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser(username='testuser')
        WorkerFactory()

    def test_organizations_list_page(self):
        url = reverse('organizations_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organizations_list.html')

    def test_organization_create_page(self):
        url = reverse('organization_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organization_create.html')

    def test_organization_detail_page(self):
        url = reverse('organization_detail', kwargs={'pk': Organization.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organization_detail.html')

    def test_organization_edit_page(self):
        url = reverse('organization_edit', kwargs={'pk': Organization.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organization_edit.html')

    def test_organization_files_list_page(self):
        url = reverse('organization_files_list', kwargs={'pk': Organization.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organization_files.html')

    def test_organization_file_create_page(self):
        url = reverse('organization_file_create', kwargs={'pk': Organization.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/organization_file_create.html')

    def test_workers_list_page(self):
        url = reverse('workers_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/workers_list.html')

    def test_worker_create_page(self):
        url = reverse('worker_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/worker_create.html')

    def test_worker_detail_page(self):
        url = reverse('worker_detail', kwargs={'pk': Worker.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/worker_detail.html')

    def test_worker_edit_page(self):
        url = reverse('worker_edit', kwargs={'pk': Worker.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_organizations/worker_edit.html')
