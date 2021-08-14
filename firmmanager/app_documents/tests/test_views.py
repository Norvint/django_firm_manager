from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import User
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.test import TestCase
from django.urls import reverse

from app_crm.models import ContractorStatus, TypeOfContractor, FieldOfActivity, Contractor
from app_documents.models import ContractType, Currency, Contract, DeliveryConditions, PaymentConditions, Order, \
    OrderWithoutContract
from app_organizations.models import Organization
from app_storage.models import ProductType, PackageInsideType, PackageOutsideType, Product, Store, \
    ProductStoreOrderBooking, ProductStoreOrderWCBooking, ProductStore
from app_users.models import Cart, CartProduct


class DocumentsViewsTest(TestCase):
    def setUp(self) -> None:
        self.client.force_login(User.objects.get(username='testuser'))

    @classmethod
    def setUpTestData(cls):
        cls.user: User = User.objects.create_superuser(username='testuser')
        cls.contract_type: ContractType = ContractType.objects.create(title='Договор продажи')
        cls.currency: Currency = Currency.objects.create(title='Рубль', code='443', char_code='RUB', nominal=1, cost=1)
        cls.contractor_status: ContractorStatus = ContractorStatus.objects.create(title='Новый')
        cls.type_of_contractor: TypeOfContractor = TypeOfContractor.objects.create(title='Клиент')
        cls.field_of_activity: FieldOfActivity = FieldOfActivity.objects.create(title='Ретейлер')
        cls.contractor: Contractor = Contractor.objects.create(
            pk=1, title='Юр. наименование контрагента', status=cls.contractor_status,
            type_of_contractor=cls.type_of_contractor, field_of_activity=cls.field_of_activity, position='Директор',
            name='Иван', last_name='Иванов', country='Россия', tel='88888888888',
            legal_address='г. Санкт-Петербург, ул. Строителей, д. 5', responsible=cls.user)
        cls.organization: Organization = Organization.objects.create(
            title='Организация поставщик', tin='123498765487', kpp='185498765421', pprnie='185498762635421',
            legal_address='г. Ростов-На-Дону, ул. Красноармейская, д. 12', requisites='Банковские реквизиты')
        cls.contract: Contract = Contract.objects.create(
            number='2021-001', type=cls.contract_type, contractor=cls.contractor, created=datetime.now(),
            organization=cls.organization, currency=cls.currency, to_delete=False, responsible=cls.user)
        cls.delivery_conditions: DeliveryConditions = DeliveryConditions.objects.create(
            title='Условие поставки', description='Описание условия поставки')
        cls.payment_conditions: PaymentConditions = PaymentConditions.objects.create(
            title='Название условия оплаты', description='Описание условия поставки')
        cls.order: Order = Order.objects.create(
            number='2021-001', contract=cls.contract, created=datetime.now(), delivery_time=3,
            delivery_conditions=cls.delivery_conditions, payment_conditions=cls.payment_conditions,
            delivery_address='г. Санкт-Петербург, ул. Строителей, д. 5', shipment_mark=None, counted_sum=0,
            currency_counted_sum=0, total_sum=0, currency_total_sum=0, to_delete=False, responsible=cls.user)
        cls.type_of_product: ProductType = ProductType.objects.create(title='Расходник')
        cls.packing_inside: PackageInsideType = PackageInsideType.objects.create(title='Пенопластовая подложка')
        cls.packing_outside: PackageOutsideType = PackageOutsideType.objects.create(title='Гофрокороб картонный')
        cls.product: Product = Product.objects.create(
            number='2324AS43S', type_of_product=cls.type_of_product, model='Tester', size='Маленький', version='1',
            materials='Металлы', color='Серебряный', packing_inside=cls.packing_inside, cost=1000, country='Россия',
            packing_outside=cls.packing_outside, description='Описание', description_en='Описание англ.')
        cls.store: Store = Store.objects.create(title='Первый склад', address='Щелковское шоссе, 1')
        cls.booking: ProductStoreOrderBooking = ProductStoreOrderBooking.objects.create(
            order=cls.order, product=cls.product, store=cls.store, quantity=10, total_price=1100,
            standard_price=cls.product.cost, counted_sum=10000, total_sum=11000)
        cls.order_wc: OrderWithoutContract = OrderWithoutContract.objects.create(
            number='2021-001', created=datetime.now(), contractor=cls.contractor, organization=cls.organization,
            currency=cls.currency, delivery_conditions=cls.delivery_conditions, delivery_time=5,
            delivery_address='г. Москва, ул. Первая, д.7', payment_conditions=cls.payment_conditions,
            shipment_mark=None, counted_sum=0, total_sum=0, to_delete=False, responsible=cls.user)
        cls.booking_wc: ProductStoreOrderWCBooking = ProductStoreOrderWCBooking.objects.create(
            order=cls.order_wc, product=cls.product, store=cls.store, quantity=10, total_price=1100,
            standard_price=cls.product.cost, counted_sum=10000, total_sum=11000)
        cls.product_in_store: ProductStore = ProductStore.objects.create(
            store=cls.store, product=cls.product, quantity=200, booked=10)
        cls.product_in_cart: CartProduct = CartProduct.objects.create(
            cart=Cart.objects.get(user=User.objects.get(username='testuser')),
            product=cls.product, store=cls.store, quantity=10)

    def test_create_contract_view(self):
        url = reverse('contract_create', kwargs={'contractor_pk': self.contractor.pk})
        response = self.client.post(url, data={'number': 'auto', 'type': self.contract_type.pk,
                                               'contractor': self.contractor.pk, 'organization': self.organization.pk,
                                               'currency': self.currency.pk, 'created': '08.09.2021'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Contract.objects.all()), 2)
        self.assertEqual(Contract.objects.last().created, datetime(year=2021, month=9, day=8).date())

    def test_contract_edit_view(self):
        url = reverse('contract_edit', kwargs={'pk': self.contract.pk})
        response = self.client.post(url, data={'number': '2021-002', 'type': self.contract.type.pk,
                                               'contractor': self.contract.contractor.pk,
                                               'currency': self.contract.currency.pk,
                                               'organization': self.contract.organization.pk})
        edited_contract = Contract.objects.first()
        self.assertNotEqual(self.contract.number, edited_contract.number)
        self.assertEqual(len(Contract.objects.all()), 1)
        self.assertEqual(response.status_code, 302)

    def test_contract_to_delete_view(self):
        url = reverse('contract_to_delete', kwargs={'pk': self.contract.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.to_delete, True)
        self.client.post(url)
        self.contract.refresh_from_db()
        self.assertEqual(self.contract.to_delete, False)

    def test_contract_detail_view(self):
        self.client.logout()
        url = reverse('contract_detail', kwargs={'pk': self.contract.pk})
        response: HttpResponseRedirect = self.client.get(url)
        self.assertURLEqual(response.url, f'/users/login/?next=/documents/contracts/{self.contract.pk}/detail/')
        self.assertEqual(response.status_code, 302)

    def test_contract_type_detail_view(self):
        self.client.logout()
        url = reverse('contract_type_detail', kwargs={'pk': self.contract_type.pk})
        response: HttpResponseRedirect = self.client.get(url)
        self.assertURLEqual(response.url,
                            f'/users/login/?next=/documents/contracts/contract-types/{self.contract_type.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_currency_detail_view(self):
        self.client.logout()
        url = reverse('currency_detail', kwargs={'pk': self.currency.pk})
        response: HttpResponseRedirect = self.client.get(url)
        self.assertURLEqual(response.url, f'/users/login/?next=/documents/contracts/currencies/{self.currency.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_order_create_view(self):
        url = reverse('order_create', kwargs={'contract_pk': self.contract.pk, 'contractor_pk': self.contractor.pk})
        response = self.client.post(url, data={'number': 'auto', 'contract': self.contract.pk,
                                               'delivery_conditions': self.delivery_conditions.pk,
                                               'delivery_time': '3', 'delivery_address': 'Тестовый адрес',
                                               'payment_conditions': self.payment_conditions.pk})
        bookings = ProductStoreOrderBooking.objects.filter(order=Order.objects.last())
        cart = Cart.objects.get(user=User.objects.get(username='testuser'))
        self.assertNotEqual(len(bookings), 0)
        self.assertEqual(bookings.first().quantity, 10)
        self.assertEqual(cart.items, 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Order.objects.all()), 2)
        self.assertEqual(Order.objects.last().number, '002-2021')

    def test_order_edit_view(self):
        url = reverse('order_edit', kwargs={'pk': self.order.pk})
        new_product = Product.objects.create(
            number='DFS432FS', type_of_product=self.type_of_product, model='Tester 2', size='Средний', version='2',
            materials='Пластик', color='Серебряный', packing_inside=self.packing_inside, cost=1000, country='Россия',
            packing_outside=self.packing_outside, description='Описание', description_en='Описание англ.')
        product_in_store: ProductStore = ProductStore.objects.create(store=self.store, product=new_product,
                                                                     quantity=200, booked=0)
        response = self.client.post(url, data={'number': '2021-001', 'contract': self.order.contract.pk,
                                               'delivery_conditions': self.order.delivery_conditions.pk,
                                               'delivery_time': '4', 'delivery_address': 'Тестовый адрес',
                                               'payment_conditions': self.order.payment_conditions.pk,
                                               'form-0-product': self.booking.product.pk,
                                               'form-0-store': self.booking.store.pk, 'form-0-quantity': '9',
                                               'form-1-product': new_product.pk, 'form-1-store': self.store.pk,
                                               'form-1-quantity': '10',
                                               'form-TOTAL_FORMS': 2, 'form-INITIAL_FORMS': 1})
        self.assertEqual(response.status_code, 302)
        product_in_store.refresh_from_db()
        self.assertEqual(product_in_store.booked, 10)
        self.assertEqual(len(self.order.bookings.all()), 2)

    def test_order_booking_delete_view(self):
        url = reverse('order_booking_delete', kwargs={'booking_pk': self.booking.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.order.bookings.all()), 0)

    def test_order_booking_edit_view(self):
        url = reverse('order_booking_edit', kwargs={'booking_pk': self.booking.pk})
        response = self.client.post(url, data={'order': self.order.pk, 'product': self.product.pk,
                                               'store': self.store.pk, 'quantity': '9', 'total_price': 1200})
        self.assertEqual(response.status_code, 302)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.total_sum, Decimal(10800))

    def test_order_without_contract_create_view(self):
        url = reverse('order_without_contract_create', kwargs={'contractor_pk': self.contractor.pk})
        response = self.client.post(url, data={'number': 'auto', 'contractor': self.contractor.pk,
                                               'organization': self.organization.pk, 'currency': self.currency.pk,
                                               'delivery_conditions': self.delivery_conditions.pk,
                                               'delivery_time': '3', 'delivery_address': 'Тестовый адрес',
                                               'payment_conditions': self.payment_conditions.pk})
        bookings = ProductStoreOrderWCBooking.objects.filter(order=OrderWithoutContract.objects.last())
        cart = Cart.objects.get(user=User.objects.get(username='testuser'))
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(len(bookings), 0)
        self.assertEqual(bookings.first().quantity, 10)
        self.assertEqual(cart.items, 0)
        self.assertEqual(len(OrderWithoutContract.objects.all()), 2)
        self.assertEqual(OrderWithoutContract.objects.last().number, '002-2021')

    def test_order_without_contract_edit_view(self):
        url = reverse('order_without_contract_edit', kwargs={'pk': self.order_wc.pk})
        new_product = Product.objects.create(
            number='DFS432FS', type_of_product=self.type_of_product, model='Tester 2', size='Средний', version='2',
            materials='Пластик', color='Серебряный', packing_inside=self.packing_inside, cost=1000, country='Россия',
            packing_outside=self.packing_outside, description='Описание', description_en='Описание англ.')
        product_in_store: ProductStore = ProductStore.objects.create(store=self.store, product=new_product,
                                                                     quantity=200, booked=0)
        response = self.client.post(url, data={'number': 'auto', 'contractor': self.contractor.pk,
                                               'organization': self.organization.pk, 'currency': self.currency.pk,
                                               'delivery_conditions': self.delivery_conditions.pk,
                                               'delivery_time': '3', 'delivery_address': 'Тестовый адрес',
                                               'payment_conditions': self.payment_conditions.pk,
                                               'form-0-product': self.booking.product.pk,
                                               'form-0-store': self.booking.store.pk, 'form-0-quantity': '9',
                                               'form-1-product': new_product.pk, 'form-1-store': self.store.pk,
                                               'form-1-quantity': '10',
                                               'form-TOTAL_FORMS': 2, 'form-INITIAL_FORMS': 1})
        self.assertEqual(response.status_code, 302)
        product_in_store.refresh_from_db()
        self.assertEqual(product_in_store.booked, 10)
        self.assertEqual(len(self.order_wc.bookings.all()), 2)

    def test_order_without_contract_to_delete_view(self):
        url = reverse('order_without_contract_to_delete', kwargs={'pk': self.order_wc.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.order_wc.refresh_from_db()
        self.assertEqual(self.order_wc.to_delete, True)
        self.client.post(url)
        self.order_wc.refresh_from_db()
        self.assertEqual(self.order_wc.to_delete, False)

    def test_order_without_contract_booking_delete_view(self):
        url = reverse('order_without_contract_booking_delete', kwargs={'booking_pk': self.booking_wc.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(self.order_wc.bookings.all()), 0)

    def test_order_without_contract_booking_edit_view(self):
        url = reverse('order_without_contract_booking_edit', kwargs={'booking_pk': self.booking_wc.pk})
        response = self.client.post(url, data={'order': self.order_wc.pk, 'product': self.product.pk,
                                               'store': self.store.pk, 'quantity': '1', 'total_price': 1200})
        self.assertEqual(response.status_code, 302)
        self.booking_wc.refresh_from_db()
        self.assertEqual(self.booking_wc.total_sum, Decimal(1200))
