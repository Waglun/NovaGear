from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from ..catalog.models import Product
from ..wishlist.models import Wishlist


@login_required
def wishlist(request):
    wishlist_ids = set(request.user.wishlist.values_list('product_id', flat=True))
    product = Product.objects.filter(wishlist_by__user=request.user) # Через модель товаров обращаемся к полю product модели wishlist
    context = {
        'wishlist_ids':wishlist_ids,
        'products':product,
    }

    return render(request, 'wishlist.html', context)


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    obj, create = Wishlist.objects.get_or_create(user=request.user, product=product)

    if not create:
        obj.delete()

    return redirect(request.META.get('HTTP_REFERER', 'catalog:catalog'))