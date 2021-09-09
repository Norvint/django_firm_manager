from decimal import Decimal

import factory

from app_storage.models import ProductType, PackageInsideType, PackageOutsideType, Product, Store, ProductStore, \
    ProductStoreOutcomeReason


class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    title = 'Тестовый тип продукции'


class PackageInsideTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PackageInsideType

    title = 'Тестовая внутренняя упаковка'


class PackageOutsideTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PackageOutsideType

    title = 'Тестовая наружная упаковка'


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    number = 'Номер'
    type_of_product = factory.SubFactory(ProductTypeFactory)
    model = 'Модель'
    size = 'Размер'
    version = 'Версия'
    materials = 'Материалы'
    color = 'Цвет'
    packing_inside = factory.SubFactory(PackageInsideTypeFactory)
    packing_outside = factory.SubFactory(PackageOutsideTypeFactory)
    country = 'Страна'
    cost = Decimal(100)


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    title = 'Тестовый склад'


class ProductStoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductStore

    store = factory.SubFactory(StoreFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = 1000
    booked = 0


class ProductStoreOutcomeReasonFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductStoreOutcomeReason

    title = 'Тестовая причина'

