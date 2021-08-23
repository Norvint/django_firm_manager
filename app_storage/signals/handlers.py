from django.db.models.signals import pre_save
from django.dispatch import receiver

from app_storage.models import ProductStoreOrderBooking, ProductStoreOrderWCBooking


@receiver(pre_save, sender=ProductStoreOrderBooking)
def recalculate_amounts(sender, instance: ProductStoreOrderBooking, **kwargs):
    instance.counted_sum = instance.standard_price * instance.quantity
    instance.total_sum = instance.total_price * instance.quantity


@receiver(pre_save, sender=ProductStoreOrderWCBooking)
def recalculate_amounts(sender, instance: ProductStoreOrderWCBooking, **kwargs):
    instance.counted_sum = instance.standard_price * instance.quantity
    instance.total_sum = instance.total_price * instance.quantity