from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from apps.cart.models import Cart

from .forms import OrderForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related('product')
    total_price = cart.total_price

    if not cart_items:
        return redirect('cart:cart')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    user=request.user,
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    comment=form.cleaned_data['comment'],
                    total_price=form.cleaned_data['total_price'],
                )

                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        price=item.product.price,
                        quantity=item.quantity,
                    )

                cart.items.all().delete()

            return redirect('orders:order_detail', order_id=order.id)

    else:
        form = OrderForm()

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)



