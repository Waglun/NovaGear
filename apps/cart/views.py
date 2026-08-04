from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .models import CartItem, Cart
from .session import SessionCart
from ..catalog.models import Product


# @login_required
def cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)

        cart_items = cart.items.select_related('product')
        total_price = cart.total_price
        total_item = cart.total_item
        is_empty = not cart_items.exists()

    else:
        session_cart = SessionCart(request)

        cart_items = session_cart.items()
        total_price = session_cart.total_price()
        total_item = session_cart.total_item()
        is_empty = session_cart.is_empty()

    shipping = 0 if total_price >= 5000 else 1200

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_item': total_item,
        'is_empty': is_empty,
        'shipping': shipping,
    }

    return render(request, 'cart.html', context)


# @login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save(update_fields=["quantity"])
    else:
        session_cart = SessionCart(request)
        session_cart.add(product.id)

    return redirect(request.META.get("HTTP_REFERER", "catalog:catalog",))


# @login_required
@require_POST
def update_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    action = request.POST.get('action')
    if action == 'increment':
        cart_item.quantity += 1
        cart_item.save(update_fields=["quantity"])
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save(update_fields=["quantity"])
        else:
            cart_item.delete()

    return redirect(request.META.get("HTTP_REFERER", "cart:cart",))



@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    cart_item.delete()

    return redirect("cart:cart")