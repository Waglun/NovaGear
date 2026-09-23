from django.shortcuts import render

from apps.catalog.models import Product


def home(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand').order_by('-time_created')[:8]

    wishlist_ids = (
        set(request.user.wishlist.values_list("product_id", flat=True))
        if request.user.is_authenticated
        else set()
    )

    context = {
        'products': products,
        'wishlist_ids': wishlist_ids,
    }

    return render(request, 'home.html', context)
