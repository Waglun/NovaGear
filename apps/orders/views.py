from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from apps.cart.models import Cart

from .forms import OrderForm, PaymentForm
from .models import Order, OrderItem


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return redirect('cart:cart')

    total_price = cart.total_price
    shipping = 0 if total_price >= 5000 else 1200
    grand_total = total_price + shipping

    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                cart_items = cart.items.select_related('product').select_for_update()

                for item in cart_items:
                    if item.product.stock < item.quantity:
                        messages.error(
                            request,
                            f'Недостаточно товара "{item.product.name}" на складе. '
                            f'Доступно: {item.product.stock}, '
                            f'запрошено: {item.quantity}.'
                        )
                        return redirect('cart:cart')

                order = Order.objects.create(
                    user=request.user,
                    address=form.cleaned_data['address'],
                    phone=form.cleaned_data['phone'],
                    comment=form.cleaned_data['comment'],
                    total_price=total_price,
                    grand_total=grand_total
                )

                for item in cart_items:
                    item.product.stock -= item.quantity
                    item.product.save()

                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        product_name=item.product.name,
                        price=item.product.price,
                        quantity=item.quantity,
                    )

                cart.items.all().delete()

            return redirect('orders:payment', order_id=order.id)

    else:
        form = OrderForm()

    cart_items = cart.items.select_related('product')

    context = {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping': shipping,
        'grand_total': grand_total,
    }

    return render(request, 'checkout.html', context)



@login_required
def order_detail(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user,
    )

    shipping = order.grand_total - order.total_price

    return render(
        request,
        'order_detail.html',
        {'order': order, 'shipping': shipping},
    )

@login_required
def payment(request, order_id):
    order = get_object_or_404(
        Order.objects.prefetch_related('items__product'),
        id=order_id,
        user=request.user,
    )

    grand_total = order.grand_total
    total_price = order.total_price
    shipping = 'Бесплатно' if total_price >= 5000 else '1200 ₽'

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                pass

            return redirect('accounts:profile', order_id=order_id)

    else:
        form = PaymentForm()

    context = {
        'form': form,
        'order': order,
        'total_price': total_price,
        'grand_total': grand_total,
        'shipping': shipping,
    }

    return render(request, 'payment.html' , context)