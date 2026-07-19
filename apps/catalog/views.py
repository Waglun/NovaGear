from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Product, Category, Brand


def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    categories = Category.objects.all()
    brands = Brand.objects.all().order_by('name')

    search_query = request.GET.get('search')
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    sort = request.GET.get('sort', 'featured')

    breadcrumbs = [
        {'name': 'Home', 'url': 'core:home'},
        {'name': 'Catalog', 'url': None},
    ]

    if search_query:
        products = products.filter(name__icontains=search_query)

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if brand_slug:
        products = products.filter(brand__slug=brand_slug)

    if sort == 'price-asc':
        products = products.order_by('price')
    elif sort == 'price-desc':
        products = products.order_by('-price')
    elif sort == 'new':
        products = products.order_by('-time_created')
    else:
        products = products.order_by('-time_created')

    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'category_slug': category_slug,
        'brand_slug': brand_slug,
        'sort': sort,
        'search_query': search_query,
        'breadcrumbs': breadcrumbs,
    }

    return render(
        request,
        'catalog.html',
        context
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related('brand', 'category')
                        .prefetch_related('images', 'attributes'),
        slug=slug
    )

    quick_specs = []
    description_bullets = []
    table_specs = []
    extra_bullets = []
    breadcrumbs = [
        {'name': 'Home', 'url': 'core:home'},
        {'name': 'Catalog', 'url': 'catalog:catalog'},
        {'name': product.name, 'url': None},
    ]

    for attr in product.attributes.all():
        if attr.sort_order == 1:
            quick_specs.append(attr)
        if attr.sort_order == 2:
            description_bullets.append(attr)
        if attr.sort_order < 3:
            table_specs.append(attr)
        if attr.sort_order == 3:
            extra_bullets.append(attr)

    context = {
        'product': product,
        'quick_specs': quick_specs,
        'description_bullets': description_bullets,
        'table_specs': table_specs,
        'extra_bullets': extra_bullets,
        'breadcrumbs': breadcrumbs,
    }

    return render(request, 'product_detail.html', context)


