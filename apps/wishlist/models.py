from django.contrib.auth import get_user_model
from django.db import models

from ..catalog.models import Product


class Wishlist(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="wishlist")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="wishlist_by")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")  # Комбинация полей должна быть уникальной. Один пользователь не может добавить товар дважды
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} -> {self.product}"