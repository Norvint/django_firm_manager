from decimal import Decimal

from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.test import TestCase
from django.urls import reverse

from app_storage.models import Product, Store, ProductStore
from app_storage.tests.factories import ProductStoreFactory, ProductStoreOutcomeReasonFactory


class StorageViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username='testuser')
        ProductStoreFactory()

    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    def test_product_create_view(self):
        url = reverse('product_create')
        response = self.client.post(url, data={'number': '001', 'model': '045', 'size': 'Большой',
                                               'version': '2', 'materials': 'Сталь',
                                               'type_of_product': 4,
                                               'color': 'Черный', 'packing_inside': 4,
                                               'packing_outside': 4, 'country': 'Россия',
                                               'cost': 1000})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Product.objects.all()), 2)

    def test_product_edit_view(self):
        url = reverse('product_edit', kwargs={'pk': Product.objects.first().pk})
        product = model_to_dict(Product.objects.first())
        product['cost'] = 999
        response = self.client.post(url, data=product)
        changed_product = Product.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(Decimal(1000), changed_product.cost)

    def test_store_outcome_create_view(self):
        product_on_store = ProductStore.objects.first()
        reason = ProductStoreOutcomeReasonFactory()
        url = reverse('store_outcome_create', kwargs={'pk': Store.objects.first().pk})
        response = self.client.post(url, data={'form-0-store': product_on_store.store.pk,
                                               'form-0-product': product_on_store.product.pk,
                                               'form-0-quantity': 10, 'form-0-reason': reason.pk,
                                               'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        product_on_store.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(product_on_store.quantity, 1000)

    def test_store_income_create_view(self):
        product_on_store = ProductStore.objects.first()
        url = reverse('store_income_create', kwargs={'pk': Store.objects.first().pk})
        response = self.client.post(url, data={'form-0-store': product_on_store.store.pk,
                                               'form-0-product': product_on_store.product.pk,
                                               'form-0-quantity': 10, 'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0})
        product_on_store.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(product_on_store.quantity, 1000)
