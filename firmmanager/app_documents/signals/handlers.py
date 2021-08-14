from django.db.models import Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver

from app_documents.models import OrderWithoutContract
from app_storage.models import Order, ProductStoreOrderBooking, ProductStoreOrderWCBooking


@receiver(pre_save, sender=Order)
def recalculate_amounts(sender, instance: Order, **kwargs):
    instance.total_sum = 0
    instance.counted_sum = 0
    bookings = ProductStoreOrderBooking.objects.filter(order=instance)
    for booking in bookings:
        instance.total_sum += booking.total_sum
        instance.counted_sum += booking.counted_sum
    instance.currency_total_sum = instance.total_sum * \
        (instance.contract.currency.nominal / instance.contract.currency.cost)
    instance.currency_counted_sum = instance.counted_sum * \
        (instance.contract.currency.nominal / instance.contract.currency.cost)


@receiver(pre_save, sender=OrderWithoutContract)
def recalculate_amounts(sender, instance: OrderWithoutContract, **kwargs):
    instance.total_sum = 0
    instance.counted_sum = 0
    bookings = ProductStoreOrderWCBooking.objects.filter(order=instance)
    for booking in bookings:
        instance.total_sum += booking.total_sum
        instance.counted_sum += booking.counted_sum
    instance.currency_total_sum = instance.total_sum * \
        (instance.currency.nominal / instance.currency.cost)
    instance.currency_counted_sum = instance.counted_sum * \
        (instance.currency.nominal / instance.currency.cost)
