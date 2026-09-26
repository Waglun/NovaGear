from django.shortcuts import render
from django.db.models import Count, Q

from apps.catalog.models import Product
from apps.core.models import HeroBanner
from apps.catalog.models import Category


def home(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand').order_by('-time_created')[:8]

    hero = HeroBanner.objects.filter(is_active=True).select_related('product_1', 'product_2').first()

    categories = Category.objects.annotate(product_count=Count('products', filter=Q(products__is_active=True)))[:8]

    wishlist_ids = (
        set(request.user.wishlist.values_list("product_id", flat=True))
        if request.user.is_authenticated
        else set()
    )

    context = {
        'products': products,
        'wishlist_ids': wishlist_ids,
        'hero': hero,
        'categories': categories,
    }

    return render(request, 'home.html', context)
