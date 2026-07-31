from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import CartItem, Cart
from ..catalog.models import Product


@login_required
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related('product')
    total_price = cart.total_price
    total_item = cart.total_item
    Shipping = 0 if total_price >= 5000 else 1200

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_item': total_item,
        'is_empty': not cart_items.exists(),
        'shipping': Shipping,
    }

    return render(request, 'cart.html', context)


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,)

    if not created:
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])

    return redirect(request.META.get("HTTP_REFERER", "catalog:catalog",))