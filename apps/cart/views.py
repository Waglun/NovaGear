from django.shortcuts import render

from .models import CartItem, Cart


def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related('product')
    total_price = cart.total_price
    total_item = cart.total_item

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_item': total_item,
        'is_empty': not cart_items.exists(),
    }

    return render(request, 'cart.html', context)