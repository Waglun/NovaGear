from django.contrib import admin
from .models import HeroBanner


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'product_1',
        'product_2',
        'is_active',
    )

    list_filter = (
        'is_active',
    )

    search_fields = (
        'title',
        'product_1__name',
        'product_2__name',
    )

    list_editable = (
        'is_active',
    )

    autocomplete_fields = (
        'product_1',
        'product_2',
    )