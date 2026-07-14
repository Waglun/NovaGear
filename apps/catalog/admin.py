from django.contrib import admin

from .models import Product, Category, Brand, ProductAttribute, ProductImage

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductAttribute)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    max_num = 10


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductAttributeInline,
    ]

    list_display = [
        "name",
        "brand",
        "price",
        "category",
        "stock",
        "is_active",
    ]

    list_filter = [
        "brand",
        "category",
        "is_active",
    ]

    search_fields = [
        "name",
        "sku",
    ]

    prepopulated_fields = {"slug": ("name",)}

