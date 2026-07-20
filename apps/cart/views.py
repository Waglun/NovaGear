from django.shortcuts import render

from .models import CartItem


def cart(request):
    cart_user = request.get('cart')
    cart_items = CartItem.objects.filter(cart=cart_user).select_related('product')

    context = {
        'cart_items': cart_items,
    }

    return render(request, 'cart.html', context)