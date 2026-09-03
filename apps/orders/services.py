from django.db import transaction

def release_order_stock(order):
    with transaction.atomic():
        items = order.items.select_related('product').select_for_update()

        for item in items:
            if item.stock_released:
                continue

            item.product.stock += item.quantity
            item.product.save(update_fields=['stock'])

            item.stock_released = True
            item.save(update_fields=['stock_released'])