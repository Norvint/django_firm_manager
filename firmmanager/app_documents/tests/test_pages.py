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
        user = User.objects.create_superuser(username='testuser')
        contract_type = ContractType(title='Договор продажи')
        contract_type.save()
        currency = Currency(title='Рубль', code='443', char_code='RUB', nominal=1, cost=1)
        currency.save()
        contractor_status = ContractorStatus(title='Новый')
        contractor_status.save()
        type_of_contractor = TypeOfContractor(title='Клиент')
        type_of_contractor.save()
        field_of_activity = FieldOfActivity(title='Ретейлер')
        field_of_activity.save()
        contractor = Contractor(
            pk=1, title='Юр. наименование контрагента', status=contractor_status, type_of_contractor=type_of_contractor,
            field_of_activity=field_of_activity, position='Директор', name='Иван', last_name='Иванов', country='Россия',
            tel='88888888888', legal_address='г. Санкт-Петербург, ул. Строителей, д. 5', responsible=user)
        contractor.save()
        organization = Organization(title='Организация поставщик', tin='123498765487', kpp='185498765421',
                                    legal_address='г. Ростов-На-Дону, ул. Красноармейская, д. 12',
                                    pprnie='185498762635421', requisites='Банковские реквизиты')
        organization.save()
        contract = Contract(number='2021-001', type=contract_type, contractor=contractor, created=datetime.now(),
                            organization=organization, currency=currency, to_delete=False, responsible=user)
        contract.save()
        delivery_conditions = DeliveryConditions(title='Условие поставки', description='Описание условия поставки')
        delivery_conditions.save()
        payment_conditions = PaymentConditions(title='Название условия оплаты', description='Описание условия поставки')
        payment_conditions.save()
        order = Order(number='2021-001', contract=contract, created=datetime.now(),
                      delivery_conditions=delivery_conditions, delivery_time=3, payment_conditions=payment_conditions,
                      delivery_address='г. Санкт-Петербург, ул. Строителей, д. 5', shipment_mark=None,
                      counted_sum=0, currency_counted_sum=0, total_sum=0, currency_total_sum=0,
                      to_delete=False, responsible=user)
        order.save()
        type_of_product = ProductType(title='Расходник')
        type_of_product.save()
        packing_inside = PackageInsideType(title='Пенопластовая подложка')
        packing_inside.save()
        packing_outside = PackageOutsideType(title='Гофрокороб картонный')
        packing_outside.save()
        product = Product(number='2324AS43S', type_of_product=type_of_product, model='Tester', size='Маленький',
                          version='1', materials='Металлы', color='Серебряный', packing_inside=packing_inside,
                          packing_outside=packing_outside, country='Россия', cost=1000, description='Описание',
                          description_en='Описание англ.')
        product.save()
        store = Store(title='Первый склад', address='Щелковское шоссе, 1')
        store.save()
        booking = ProductStoreOrderBooking(order=order, product=product, store=store, quantity=10, total_price=1100,
                                           standard_price=product.cost, counted_sum=10000,
                                           currency_counted_sum=10000, total_sum=11000,
                                           currency_total_sum=11000)
        booking.save()
        order_wc = OrderWithoutContract(number='2021-001', created=datetime.now(), contractor=contractor,
                                        organization=organization, currency=currency,
                                        delivery_conditions=delivery_conditions, delivery_time=5,
                                        delivery_address='г. Москва, ул. Первая, д.7',
                                        payment_conditions=payment_conditions, shipment_mark=None,
                                        counted_sum=0, total_sum=0, to_delete=False, responsible=user)
        order_wc.save()
        booking_wc = ProductStoreOrderWCBooking(order=order_wc, product=product, store=store, quantity=10,
                                                total_price=1100, standard_price=product.cost, counted_sum=10000,
                                                total_sum=11000)
        booking_wc.save()

    def test_contracts_list_page(self):
        url = reverse('contracts_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contracts_list.html')

    def test_contract_create_page(self):
        url = reverse('contract_create', kwargs={'contractor_id': '0'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_create.html')

    def test_contract_detail_page(self):
        contract = Contract.objects.all().first()
        url = reverse('contract_detail', kwargs={'pk': contract.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_detail.html')

    def test_contract_edit_page(self):
        contract = Contract.objects.all().first()
        url = reverse('contract_edit', kwargs={'pk': contract.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_edit.html')

    def test_contract_types_list_page(self):
        url = reverse('contract_types_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_types_list.html')

    def test_contract_type_detail_page(self):
        contract_type = ContractType.objects.all().first()
        url = reverse('contract_type_detail', kwargs={'pk': contract_type.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/contract_type_detail.html')

    def test_currencies_list_page(self):
        url = reverse('currencies_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/currencies_list.html')

    def test_currency_detail_page(self):
        currency = Currency.objects.all().first()
        url = reverse('currency_detail', kwargs={'pk': currency.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/contracts/currency_detail.html')

    def test_orders_list_page(self):
        url = reverse('orders_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/orders_list.html')

    def test_order_create_page(self):
        contract = Contract.objects.all().first()
        url = reverse('order_create', kwargs={'contract_id': contract.pk, 'contractor_id': contract.contractor.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_create.html')

    def test_order_detail_page(self):
        order = Order.objects.all().first()
        url = reverse('order_detail', kwargs={'pk': order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_detail.html')

    def test_order_edit_page(self):
        order = Order.objects.all().first()
        url = reverse('order_edit', kwargs={'pk': order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_edit.html')

    def test_order_booking_create_page(self):
        order = Order.objects.all().first()
        url = reverse('order_booking', kwargs={'pk': order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_booking_create.html')

    def test_order_booking_edit_page(self):
        booking = ProductStoreOrderBooking.objects.all().last()
        url = reverse('order_booking_edit', kwargs={'pk': booking.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/order_booking_edit.html')

    def test_delivery_conditions_list_page(self):
        url = reverse('delivery_conditions_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders/delivery_conditions_list.html')

    def test_delivery_condition_detail_page(self):
        delivery_condition = DeliveryConditions.objects.all().first()
        url = reverse('delivery_condition_detail', kwargs={'pk': delivery_condition.pk})
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
        order_wc = OrderWithoutContract.objects.all().first()
        url = reverse('order_without_contract_detail', kwargs={'pk': order_wc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders_without_contract/order_detail.html')

    def test_order_without_contract_booking_edit_page(self):
        booking_wc = ProductStoreOrderWCBooking.objects.all().first()
        url = reverse('order_without_contract_booking_edit', kwargs={'pk': booking_wc.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'app_documents/orders_without_contract/order_booking_edit.html')



