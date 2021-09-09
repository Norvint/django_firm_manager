from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from app_organizations.models import Organization, Worker
from app_organizations.tests.factories import WorkerFactory


class OrganizationViewsTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser')
        WorkerFactory()

    def test_organization_create_view(self):
        url = reverse('organization_create')
        response = self.client.post(url, data={'title': 'Новая организация', 'tin': '124253', 'kpp': '53435234',
                                               'pprnie': '28382342', 'legal_address': 'Юр. адрес новой организации',
                                               'requisites': 'Реквизиты новой организации'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Organization.objects.all()), 2)

    def test_organization_edit_view(self):
        organization = Organization.objects.first()
        url = reverse('organization_edit', kwargs={'pk': organization.pk})
        data = model_to_dict(organization)
        data['title'] = 'Измененная организация №1'
        response = self.client.post(url, data=data)
        changed_organization = Organization.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(organization.title, changed_organization.title)

    def test_worker_create_view(self):
        url = reverse('worker_create')
        response = self.client.post(url, data={'name': 'Андрей', 'second_name': 'Андреевич', 'last_name': 'Андреев',
                                               'position': 'Помощник тестировщика',
                                               'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Worker.objects.all()), 2)

    def test_worker_edit_view(self):
        worker = Worker.objects.first()
        url = reverse('worker_edit', kwargs={'pk': worker.pk})
        data = model_to_dict(worker)
        data['name'] = 'Михаил'
        data['user'] = '6'
        response = self.client.post(url, data={**data, 'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        changed_worker = Worker.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(worker.name, changed_worker.name)
