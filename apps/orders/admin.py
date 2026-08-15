from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline): # Табличное отображение встраиваемого объекта в Order
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price', 'subtotal_price',)
    readonly_fields = ('product', 'quantity', 'price', 'subtotal_price',)
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')