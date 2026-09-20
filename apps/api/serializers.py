from rest_framework import serializers
from apps.catalog.models import Product
from apps.cart.models import CartItem
from apps.cart.models import Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'old_price', 'image', 'category', 'brand', 'stock', 'sku']


class CartItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='product.name', read_only=True)
    price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    subtotal = serializers.DecimalField(
        source='subtotal_price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'name', 'price', 'quantity', 'subtotal']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['items', 'total_price', 'total_item']


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']