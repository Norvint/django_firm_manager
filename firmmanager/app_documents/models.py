from datetime import datetime

from django.db import models

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
    description = models.CharField('Описание', max_length=200)

    class Meta:
        verbose_name = 'Условие оплаты'
        verbose_name_plural = 'Условия оплаты'

    def __str__(self):
        return self.title


class Contract(models.Model):
    number = models.CharField('Номер договора', max_length=30)
    type = models.ForeignKey(ContractType, on_delete=models.CASCADE, verbose_name='Тип договора')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE, verbose_name='Клиент')
    created = models.DateField(auto_now_add=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name='Организация поставщик')
    delivery_address = models.CharField('Место поставки', max_length=50)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, verbose_name='Валюта')
    to_delete = models.BooleanField('К удалению', default=False)

    class Meta:
        verbose_name = 'Договор'
        verbose_name_plural = 'Договоры'

    def __str__(self):
        return f'{self.pk} - {self.contractor}'


class Order(models.Model):
    number = models.CharField('Номер заказа', max_length=30, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, verbose_name='Договор')
    created = models.DateField(auto_now_add=True)
    delivery_conditions = models.ForeignKey(DeliveryConditions, on_delete=models.CASCADE,
                                            verbose_name='Условия поставки')
    delivery_time = models.IntegerField('Срок поставки, дней', default=1)
    loading_place = models.CharField('Место загрузки', max_length=100)
    payment_conditions = models.ForeignKey(PaymentConditions, on_delete=models.CASCADE,
                                           verbose_name='Условия оплаты')
    shipment_mark = models.CharField('Отгрузочная метка', max_length=100)
    total_sum = models.DecimalField('Сумма', max_digits=10, decimal_places=4, default=0)
    to_delete = models.BooleanField('К удалению', default=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'№{self.number} - {self.contract.contractor.title}'
