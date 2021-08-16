from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from app_crm.models import ContractorStatus, TypeOfContractor, FieldOfActivity, Contractor
from app_documents.models import ContractType, Currency, Contract, DeliveryConditions, Order, PaymentConditions, \
    OrderWithoutContract
from app_organizations.models import Organization
from app_storage.models import Product, ProductType, PackageInsideType, PackageOutsideType, Store, \
    ProductStoreOrderBooking, ProductStoreOrderWCBooking


class DocumentsPagesTests(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_superuser(username='testuser')
        cls.contract_type = ContractType.objects.create(title='Договор продажи')
        cls.currency = Currency.objects.create(title='Рубль', code='443', char_code='RUB', nominal=1, cost=1)
        cls.contractor_status = ContractorStatus.objects.create(title='Новый')
        cls.type_of_contractor = TypeOfContractor.objects.create(title='Клиент')
        cls.field_of_activity = FieldOfActivity.objects.create(title='Ретейлер')
        cls.contractor = Contractor.objects.create(
            pk=1, title='Юр. наименование контрагента', status=cls.contractor_status,
            type_of_contractor=cls.type_of_contractor, field_of_activity=cls.field_of_activity, position='Директор',
            name='Иван', last_name='Иванов', country='Россия', tel='88888888888',
            legal_address='г. Санкт-Петербург, ул. Строителей, д. 5', responsible=cls.user)
        cls.organization = Organization.objects.create(title='Организация поставщик', tin='123498765487',
                                                       kpp='185498765421',
                                                       legal_address='г. Ростов-На-Дону, ул. Красноармейская, д. 12',
                                                       pprnie='185498762635421', requisites='Банковские реквизиты')
        cls.contract = Contract.objects.create(number='2021-001', type=cls.contract_type, contractor=cls.contractor,
                                               created=datetime.now(), organization=cls.organization,
                                               currency=cls.currency,
                                               to_delete=False, responsible=cls.user)
        cls.delivery_conditions = DeliveryConditions.objects.create(title='Условие поставки',
                                                                    description='Описание условия поставки')
        cls.payment_conditions = PaymentConditions.objects.create(title='Название условия оплаты',
                                                                  description='Описание условия поставки')
        cls.order = Order.objects.create(number='2021-001', contract=cls.contract, created=datetime.now(),
                                         delivery_conditions=cls.delivery_conditions, delivery_time=3,
                                         payment_conditions=cls.payment_conditions,
                                         delivery_address='г. Санкт-Петербург, ул. Строителей, д. 5',
                                         shipment_mark=None,
                                         counted_sum=0, currency_counted_sum=0, total_sum=0, currency_total_sum=0,
                                         to_delete=False, responsible=cls.user)
        cls.type_of_product = ProductType.objects.create(title='Расходник')
        cls.packing_inside = PackageInsideType.objects.create(title='Пенопластовая подложка')
        cls.packing_outside = PackageOutsideType.objects.create(title='Гофрокороб картонный')
        cls.product = Product.objects.create(number='2324AS43S', type_of_product=cls.type_of_product, model='Tester',
                                             size='Маленький', version='1', materials='Металлы', color='Серебряный',
                                             packing_inside=cls.packing_inside, packing_outside=cls.packing_outside,
                                             country='Россия', cost=1000, description='Описание',
                                             description_en='Описание англ.')
        cls.store = Store.objects.create(title='Первый склад', address='Щелковское шоссе, 1')
        cls.booking = ProductStoreOrderBooking.objects.create(order=cls.order, product=cls.product, store=cls.store,
                                                              quantity=10,
                                                              total_price=1100, standard_price=cls.product.cost,
                                                              counted_sum=10000, total_sum=11000)
        cls.order_wc = OrderWithoutContract.objects.create(number='2021-001', created=datetime.now(),
                                                           contractor=cls.contractor,
                                                           organization=cls.organization, currency=cls.currency,
                                                           delivery_conditions=cls.delivery_conditions, delivery_time=5,
                                                           delivery_address='г. Москва, ул. Первая, д.7',
                                                           payment_conditions=cls.payment_conditions,
                                                           shipment_mark=None,
                                                           counted_sum=0, total_sum=0, to_delete=False,
                                                           responsible=cls.user)
        cls.booking_wc = ProductStoreOrderWCBooking.objects.create(order=cls.order_wc, product=cls.product,
                                                                   store=cls.store,
                                                                   quantity=10, total_price=1100,
                                                                   standard_price=cls.product.cost, counted_sum=10000,
                                                                   total_sum=11000)

    def test_contracts_list_page(self):
        url = reverse('contracts_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contracts_list.html')

    def test_contract_create_page(self):
        url = reverse('contract_create', kwargs={'contractor_pk': '0'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_create.html')

    def test_contract_detail_page(self):
        url = reverse('contract_detail', kwargs={'pk': self.contract.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_detail.html')

    def test_contract_edit_page(self):
        url = reverse('contract_edit', kwargs={'pk': self.contract.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_edit.html')

    def test_contract_types_list_page(self):
        url = reverse('contract_types_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_types_list.html')

    def test_contract_type_detail_page(self):
        url = reverse('contract_type_detail', kwargs={'pk': self.contract_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_type_detail.html')

    def test_currencies_list_page(self):
        url = reverse('currencies_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/currencies_list.html')

    def test_currency_detail_page(self):
        url = reverse('currency_detail', kwargs={'pk': self.currency.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/currency_detail.html')

    def test_orders_list_page(self):
        url = reverse('orders_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/orders_list.html')

    def test_order_create_page(self):
        url = reverse('order_create', kwargs={'contract_pk': self.contract.pk,
                                              'contractor_pk': self.contract.contractor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_create.html')

    def test_order_detail_page(self):
        url = reverse('order_detail', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_detail.html')

    def test_order_edit_page(self):
        url = reverse('order_edit', kwargs={'pk': self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_edit.html')

    def test_order_booking_edit_page(self):
        url = reverse('order_booking_edit', kwargs={'booking_pk': self.booking.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_booking_edit.html')

    def test_delivery_conditions_list_page(self):
        url = reverse('delivery_conditions_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/delivery_conditions_list.html')

    def test_delivery_condition_detail_page(self):
        url = reverse('delivery_condition_detail', kwargs={'pk': self.delivery_conditions.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/delivery_condition_detail.html')

    def test_payment_conditions_list_page(self):
        url = reverse('payment_conditions_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/payment_conditions_list.html')

    def test_orders_without_contract_list_page(self):
        url = reverse('orders_without_contract_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders_without_contract/orders_list.html')

    def test_order_without_contract_detail_page(self):
        url = reverse('order_without_contract_detail', kwargs={'pk': self.order_wc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders_without_contract/order_detail.html')

    def test_order_without_contract_booking_edit_page(self):
        url = reverse('order_without_contract_booking_edit', kwargs={'booking_pk': self.booking_wc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders_without_contract/order_booking_edit.html')
