from django.contrib.auth import get_user_model
from django.db import models

from apps.catalog.models import Product


class Order(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=[
        ('created', 'Pending'),
        ('paid', 'Canceled'),
        ('supplier', 'Supplier'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ], default='created')
    address = models.TextField(max_length=120)
    phone = models.CharField(max_length=120)
    comment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal_price(self):
        if self.price is None or self.quantity is None:
            return 0

        return self.price * self.quantity

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'