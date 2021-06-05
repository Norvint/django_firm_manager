from django.contrib.auth.models import User
from django.db import models

from app_documents.models import Order, OrderWithoutContract


class ProductType(models.Model):
    title = models.CharField('Наименование', max_length=30)

    class Meta:
        verbose_name = 'Тип продукции'
        verbose_name_plural = 'Типы продукции'

    def __str__(self):
        return self.title


class PackageInsideType(models.Model):
    title = models.CharField('Наименование', max_length=40)

    class Meta:
        verbose_name = 'Вид внутренней упаковки'
        verbose_name_plural = 'Виды внутренней упаковки'

    def __str__(self):
        return self.title


class PackageOutsideType(models.Model):
    title = models.CharField('Наименование', max_length=40)

    class Meta:
        verbose_name = 'Вид внешней упаковки'
        verbose_name_plural = 'Виды внешней упаковки'

    def __str__(self):
        return self.title


class Product(models.Model):
    number = models.CharField('Артикул', max_length=40, unique=True)
    type_of_product = models.ForeignKey(ProductType, on_delete=models.CASCADE, verbose_name='Тип продукции')
    model = models.CharField('Модель', max_length=30)
    size = models.CharField('Размер', max_length=30)
    version = models.CharField('Версия', max_length=30)
    materials = models.CharField('Материалы', max_length=100)
    color = models.CharField('Цвет', max_length=30)
    packing_inside = models.ForeignKey(PackageInsideType, on_delete=models.CASCADE, verbose_name='Внутренняя упаковка')
    packing_outside = models.ForeignKey(PackageOutsideType, on_delete=models.CASCADE, verbose_name='Внешнняя упаковка')
    country = models.CharField('Страна', max_length=50)
    cost = models.DecimalField('Цена за 1 ед. в рублях', decimal_places=2, max_digits=15)
    description = models.TextField('Описание', max_length=1000, blank=True)
    description_en = models.TextField('Описание(англ)', max_length=1000, blank=True)

    class Meta:
        verbose_name = 'Продукция'
        verbose_name_plural = 'Продукция'

    def __str__(self):
        return f'{self.type_of_product}. {self.number}'


class Store(models.Model):
    title = models.CharField('Название', max_length=40)
    address = models.CharField('Адрес', max_length=100, unique=True)

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.title


class ProductStore(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    quantity = models.PositiveIntegerField('Количество')
    booked = models.IntegerField('Забронировано')

    class Meta:
        verbose_name = 'Колисчество продукции на складе'
        verbose_name_plural = 'Колисчество продукции на складах'

    def __str__(self):
        return f'{self.store} / {self.product} / {self.quantity} / {self.booked}'


class ProductStoreIncome(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    quantity = models.PositiveIntegerField('Количество')
    date = models.DateField(auto_now_add=True, verbose_name='Дата прихода')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Приход продукции на склад'
        verbose_name_plural = 'Приходы продукции на склад'

    def __str__(self):
        return f'{self.product} - {self.store} - {self.quantity}'


class ProductStoreOutcomeReason(models.Model):
    title = models.CharField('Название', max_length=300)

    class Meta:
        verbose_name = 'Причина выпуска продукции'
        verbose_name_plural = 'Причины выпуска продукции'

    def __str__(self):
        return self.title


class ProductStoreOutcome(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    quantity = models.PositiveIntegerField('Количество')
    reason = models.ForeignKey(ProductStoreOutcomeReason, on_delete=models.CASCADE, verbose_name='Причина выпуска', blank=True, null=True)
    date = models.DateField(auto_now_add=True, verbose_name='Дата выпуска')
    responsible = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    comment = models.CharField('Комментарий', max_length=1000)

    class Meta:
        verbose_name = 'Списание продукции со склада'
        verbose_name_plural = 'Списания продукции со складов'

    def __str__(self):
        return f'{self.product} - {self.store} - {self.quantity}'


class ProductStoreOrderBooking(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    quantity = models.PositiveIntegerField('Количество')
    total_price = models.DecimalField('Итоговая цена', decimal_places=2, max_digits=18, null=True, blank=True)
    standard_price = models.DecimalField('Стандартная цена', decimal_places=2, max_digits=18, null=True, blank=True)
    counted_sum = models.DecimalField('Расчетная сумма', decimal_places=2, max_digits=18, null=True, blank=True)
    total_sum = models.DecimalField('Итоговая сумма', decimal_places=2, max_digits=18, null=True, blank=True)

    class Meta:
        verbose_name = 'Бронь продукции по заказу'
        verbose_name_plural = 'Брони продукции по заказам'

    def __str__(self):
        return f'{self.product} - {self.store} - {self.quantity}'


class ProductStoreOrderWithoutContractBooking(models.Model):
    order = models.ForeignKey(OrderWithoutContract, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукция')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    quantity = models.PositiveIntegerField('Количество')
    total_price = models.DecimalField('Итоговая цена', decimal_places=2, max_digits=18, null=True, blank=True)
    standard_price = models.DecimalField('Стандартная цена', decimal_places=2, max_digits=18, null=True, blank=True)
    counted_sum = models.DecimalField('Расчетная сумма', decimal_places=2, max_digits=18, null=True, blank=True)
    total_sum = models.DecimalField('Итоговая сумма', decimal_places=2, max_digits=18, null=True, blank=True)

    class Meta:
        verbose_name = 'Бронь продукции по заказу без договора'
        verbose_name_plural = 'Брони продукции по заказам без договора'

    def __str__(self):
        return f'{self.product} - {self.store} - {self.quantity}'
