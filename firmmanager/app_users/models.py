from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from app_storage.models import Product, Store


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Корзина')
    items = models.IntegerField('Количество позиций')
    total_sum = models.DecimalField('Итоговая сумма', decimal_places=2, max_digits=18, default=0)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина пользователя {self.user}'

    @receiver(post_save, sender=User)
    def _create_new_cart_if_needed(sender, instance, **kwargs):
        try:
            cart = Cart.objects.get(user=instance)
        except Cart.DoesNotExist:
            Cart.objects.create(user=instance, items=0, total_sum=0)


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name='Склад')
    quantity = models.IntegerField('Количество')

    class Meta:
        verbose_name = 'Продукция в корзине'
        verbose_name_plural = 'Продукция в корзинах'

    def __str__(self):
        return f'{self.cart} - {self.product}'
