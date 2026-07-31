from django.contrib.auth import get_user_model
from django.db import models

from ..catalog.models import Product


class Cart(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        total_price = sum(item.subtotal_price for item in self.items.all())
        return total_price

    @property
    def total_item(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1)

    @property
    def subtotal_price(self):
        return self.product.price * self.quantity

    class Meta:
        unique_together = ('cart', 'product')

