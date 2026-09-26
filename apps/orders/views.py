from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from apps.cart.models import Cart

from .forms import OrderForm, PaymentForm
from .models import Order, OrderItem
from .services import release_order_stock


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if not cart.items.exists():
        return redirect('cart:cart')

    total_price = cart.total_price
    shipping = 0 if total_price >= 200 else 20
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
    shipping = 'Free' if total_price >= 200 else '20'

    if request.method == 'POST':

        form = PaymentForm(request.POST)

        if form.is_valid():
            payment_action = request.POST.get('payment_action')
            if payment_action == 'failed':
                with transaction.atomic():
                    order = (Order.objects.select_for_update().get(id=order_id, user=request.user))
                    release_order_stock(order)
                    order.payment_status = Order.PaymentStatus.FAILED
                    order.order_status = Order.OrderStatus.CANCELLED
                    order.save(update_fields=['payment_status', 'order_status'])

                return redirect('orders:payment_failed', order_id=order.id)

            with transaction.atomic():
                order = Order.objects.select_for_update().get(id=order_id, user=request.user)
                if order.payment_status == Order.PaymentStatus.PAID:
                    return redirect('orders:payment_success', order_id=order.id) # Если заказ уже оплачен, при повторной отправке формы произойдет редирект

                order.payment_status = Order.PaymentStatus.PAID
                order.order_status = Order.OrderStatus.PROCESSING
                order.save(update_fields=['payment_status', 'order_status'])

            return redirect('orders:payment_success', order_id=order_id)

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


@login_required
def payment_success(request, order_id):
    return render(request, 'payment_success.html', {'order_id': order_id})


@login_required
def payment_failed(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment_failed.html',{'order': order})