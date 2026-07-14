from django.shortcuts import render

from .models import Product, Category, Brand


def catalog(request):
    products = Product.objects.filter(is_active=True).select_related('category', 'brand')
    categories = Category.objects.all().order_by('name')
    brands = Brand.objects.all().order_by('name')

    search_query = request.GET.get('search')
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    sort = request.GET.get('sort', 'featured')

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
        products = products.order_by('-created_at')  # или -date_added, -id
    elif sort == 'featured':
        # Можно оставить без сортировки или сделать свою логику (например, по popularity)
        pass
    else:
        # на случай неизвестного значения
        products = products.order_by('-created_at')

    context = {
        'products': products,
        'brands': brands,
        'categories': categories,
        'products_count': products.count(),
        'category_slug': category_slug,
        'brand_slug': brand_slug,
        'sort': sort,
    }

    return render(
        request,
        'catalog.html',
        context
    )

