from django.contrib import admin
from django.utils.html import format_html

from .models import Product, Category, Brand, ProductAttribute, ProductImage

admin.site.register(Category)
admin.site.register(Brand)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    max_num = 10


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1

    fields = [
        "attribute_type",
        "name",
        "value",
        "sort_order",
    ]

    ordering = ["attribute_type", "sort_order"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductImageInline,
        ProductAttributeInline,
    ]

    list_display = [
        "image_preview",
        "name",
        "brand",
        "price",
        "category",
        "stock",
        "is_active",
    ]

    list_editable = [
        "price",
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

    ordering = ["name"]

    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="Изображение")
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="60" height="60" '
                'style="object-fit: contain; border-radius: 6px;" />',
                obj.image.url,
            )

        return "—"

