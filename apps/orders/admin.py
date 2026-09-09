from django.contrib import admin

from apps.orders.models import Order, OrderItem


class OrderItemInline(admin.TabularInline): # Табличное отображение встраиваемого объекта в Order
    model = OrderItem
    extra = 0
    fields = ('product', 'product_name', 'quantity', 'price', 'subtotal_price',)
    readonly_fields = ('product', 'product_name', 'quantity', 'price', 'subtotal_price',)
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = ('id', 'user', 'order_status', 'payment_status', 'total_price', 'grand_total', 'created_at')
    list_filter = ('order_status', 'payment_status', 'created_at')
    search_fields = ('id', 'user__email', 'user__username', 'phone')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    readonly_fields = ('user', 'total_price', 'grand_total', 'created_at', 'updated_at')

    actions = (
        'mark_as_processing',
        'mark_as_shipped',
        'cancel_orders',
    )

    @admin.action(description='Отметить выбранные заказы как "В обработке"')
    def mark_as_processing(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.PROCESSING)
        self.message_user(request, f'Заказов переведено в статус "В обработке": {updated}.')

    @admin.action(description='Отметить выбранные заказы как "Отправлен"')
    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.SHIPPED)
        self.message_user(request, f'Заказов переведено в статус "Отправлен": {updated}.')

    @admin.action(description='Отменить выбранные заказы')
    def cancel_orders(self, request, queryset):
        updated = queryset.update(order_status=Order.OrderStatus.CANCELLED)
        self.message_user(request, f'Заказов отменено: {updated}.')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price', 'subtotal_price')