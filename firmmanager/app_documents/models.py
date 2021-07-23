from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from app_crm.models import Contractor
from app_organizations.models import Organization


class ContractType(models.Model):
    title = models.CharField('Наименование', max_length=40)

    class Meta:
        verbose_name = 'Тип договора'
        verbose_name_plural = 'Типы договоров'

    def __str__(self):
        return self.title


class Currency(models.Model):
    title = models.CharField('Название', max_length=100)
    code = models.CharField('Код', max_length=20)
    char_code = models.CharField('Символьное обозначение', max_length=10)
    nominal = models.IntegerField('Номинал')
    cost = models.DecimalField('Цена', max_digits=10, decimal_places=4)

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'

    def __str__(self):
        return self.title


class DeliveryConditions(models.Model):
    title = models.CharField('Название', max_length=30)
    description = models.CharField('Описание', max_length=200)

    class Meta:
        verbose_name = 'Условие поставки'
        verbose_name_plural = 'Условия поставки'

    def __str__(self):
        return self.title


class PaymentConditions(models.Model):
    title = models.CharField('Название', max_length=30)
    description = models.CharField('Описание', max_length=1000)
    description_en = models.CharField('Описание(англ)', max_length=1000, blank=True)

    class Meta:
        verbose_name = 'Условие оплаты'
        verbose_name_plural = 'Условия оплаты'

    def __str__(self):
        return self.title


class ShipmentMark(models.Model):
    description = models.CharField('Описание', max_length=1000)
    description_en = models.CharField('Описание(англ)', max_length=1000)

    class Meta:
        verbose_name = 'Отгрузочная метка'
        verbose_name_plural = 'Отгрузочные метки'

    def __str__(self):
        return self.description


class Contract(models.Model):
    number = models.CharField('Номер договора', max_length=30)
    type = models.ForeignKey(ContractType, on_delete=models.CASCADE, verbose_name='Тип договора')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Клиент')
    created = models.DateField('Дата создания')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация поставщик')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    to_delete = models.BooleanField('К удалению', default=False)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'{self.number} - {self.contractor}'


class Order(models.Model):
    number = models.CharField('Номер заказа', max_length=30, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    created = models.DateField(auto_now_add=True)
    delivery_conditions = models.ForeignKey(DeliveryConditions, on_delete=models.CASCADE,
                                            verbose_name='Условия поставки')
    delivery_time = models.IntegerField('Срок поставки, дней', default=1)
    delivery_address = models.CharField('Место поставки', max_length=100)
    payment_conditions = models.ForeignKey(PaymentConditions, on_delete=models.CASCADE,
                                           verbose_name='Условия оплаты')
    shipment_mark = models.ForeignKey(ShipmentMark, on_delete=models.CASCADE, verbose_name='Отгрузочная метка',
                                      blank=True, null=True)
    counted_sum = models.DecimalField('Расчетная сумма', max_digits=20, decimal_places=4, default=0)
    currency_counted_sum = models.DecimalField('Расчетная сумма в валюте', max_digits=20, decimal_places=2, default=0)
    total_sum = models.DecimalField('Итоговая сумма', max_digits=20, decimal_places=4, default=0)
    currency_total_sum = models.DecimalField('Итоговая сумма в валюте', max_digits=20, decimal_places=2, default=0)
    to_delete = models.BooleanField('К удалению', default=False)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'№{self.number} - {self.contract.contractor.title}'

    def update_order(self, form_data: dict):
        if form_data.get('number'):
            self.number = form_data.get('number')
        if form_data.get('contract'):
            self.contract = form_data.get('contract')
        if form_data.get('delivery_conditions'):
            self.delivery_conditions = form_data.get('delivery_conditions')
        if form_data.get('delivery_time'):
            self.delivery_time = form_data.get('delivery_time')
        if form_data.get('delivery_address'):
            self.delivery_address = form_data.get('delivery_address')
        if form_data.get('payment_conditions'):
            self.payment_conditions = form_data.get('payment_conditions')

    def recalculate_amounts(self, bookings: QuerySet):
        self.total_sum = 0
        self.counted_sum = 0
        for booking in bookings:
            self.total_sum += booking.total_sum
            self.counted_sum += booking.counted_sum


class OrderWithoutContract(models.Model):
    number = models.CharField('Номер заказа', max_length=30, blank=True)
    created = models.DateField(auto_now_add=True)
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Клиент')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация поставщик')
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    delivery_conditions = models.ForeignKey(DeliveryConditions, on_delete=models.CASCADE,
                                            verbose_name='Условия поставки')
    delivery_time = models.IntegerField('Срок поставки, дней', default=1)
    delivery_address = models.CharField('Место поставки', max_length=100)
    payment_conditions = models.ForeignKey(PaymentConditions, on_delete=models.CASCADE,
                                           verbose_name='Условия оплаты')
    shipment_mark = models.ForeignKey(ShipmentMark, on_delete=models.CASCADE, verbose_name='Отгрузочная метка',
                                      blank=True, null=True)
    counted_sum = models.DecimalField('Расчетная сумма', max_digits=20, decimal_places=4, default=0)
    total_sum = models.DecimalField('Итоговая сумма', max_digits=20, decimal_places=4, default=0)
    to_delete = models.BooleanField('К удалению', default=False)
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Заказ без договора'
        verbose_name_plural = 'Заказы без договора'

    def __str__(self):
        return f'№{self.number} - {self.contractor.title}'

    def recalculate_amounts(self, bookings: QuerySet):
        self.total_sum = 0
        self.counted_sum = 0
        for booking in bookings:
            self.total_sum += booking.total_sum
            self.counted_sum += booking.counted_sum


