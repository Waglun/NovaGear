from django.db import models

from apps.catalog.models import Product


class HeroBanner(models.Model):
    title = models.CharField(max_length=100, blank=True)
    main_image = models.ImageField(
        upload_to='hero/',
        blank=True,
        null=True
    )
    product_1 = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hero_product_1'
    )
    product_2 = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='hero_product_2'
    )
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title or 'Hero Banner'
