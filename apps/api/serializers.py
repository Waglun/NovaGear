from rest_framework import serializers
from apps.catalog.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'old_price', 'image', 'category', 'brand', 'stock', 'sku']
