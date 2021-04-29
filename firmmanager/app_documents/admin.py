from django.contrib import admin
from django.forms import TextInput, Textarea
from django.db import models

from app_documents.models import Contract, ContractType, Currency, DeliveryConditions, PaymentConditions, Order, \
    ShipmentMark
from app_storage.models import ProductStoreOrderBooking


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'contractor', 'created', 'organization')
    list_filter = ('organization', 'currency')
    search_fields = ('number', 'client', 'organization')


@admin.register(Order)
class SpecificationAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductStoreOrderBooking)
class SpecificationBookingAdmin(admin.ModelAdmin):
    pass


@admin.register(ContractType)
class ContractTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass


@admin.register(DeliveryConditions)
class DeliveryConditionsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150em'})},
    }


@admin.register(PaymentConditions)
class PaymentConditionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '150em'})},
    }


@admin.register(ShipmentMark)
class ShipmentMarkAdmin(admin.ModelAdmin):
    pass