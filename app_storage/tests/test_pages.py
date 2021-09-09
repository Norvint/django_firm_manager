from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_storage.models import Product, Store
from app_storage.tests.factories import ProductStoreFactory


class StoragePagesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser')
        ProductStoreFactory()

    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    def test_products_list_page(self):
        url = reverse('products_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/products_list.html')

    def test_product_create_page(self):
        url = reverse('product_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_create.html')

    def test_product_detail_page(self):
        url = reverse('product_detail', kwargs={'pk': Product.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_detail.html')

    def test_product_edit_page(self):
        url = reverse('product_edit', kwargs={'pk': Product.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_edit.html')

    def test_stores_list_page(self):
        url = reverse('stores_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/stores_list.html')

    def test_store_detail_page(self):
        url = reverse('store_detail', kwargs={'pk': Store.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/store_detail.html')

    def test_store_outcome_create_page(self):
        url = reverse('store_outcome_create', kwargs={'pk': Store.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_store_outcome_create.html')

    def test_store_income_create_page(self):
        url = reverse('store_income_create', kwargs={'pk': Store.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_store_income_create.html')

    def test_store_outcome_list_page(self):
        url = reverse('store_outcome_list', kwargs={'pk': Store.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_store_outcome_list.html')

    def test_store_income_list_page(self):
        url = reverse('store_income_list', kwargs={'pk': Store.objects.first().pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_storage/product_store_income_list.html')
