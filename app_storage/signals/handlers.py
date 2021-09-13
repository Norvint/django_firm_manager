from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from app_storage.models import ProductStoreOrderBooking, ProductStoreOrderWCBooking, Cart


@receiver(post_save, sender=User)
def create_new_cart_if_needed(sender, instance, **kwargs):
    try:
        cart = Cart.objects.get(user=instance)
    except Cart.DoesNotExist:
        Cart.objects.create(user=instance, items=0, total_sum=0)


@receiver(pre_save, sender=ProductStoreOrderBooking)
def recalculate_amounts(sender, instance: ProductStoreOrderBooking, **kwargs):
    instance.counted_sum = instance.standard_price * instance.quantity
    instance.total_sum = instance.total_price * instance.quantity


@receiver(pre_save, sender=ProductStoreOrderWCBooking)
def recalculate_amounts(sender, instance: ProductStoreOrderWCBooking, **kwargs):
    instance.counted_sum = instance.standard_price * instance.quantity
    instance.total_sum = instance.total_price * instance.quantity