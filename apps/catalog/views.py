from django.shortcuts import render

from .models import Product, Category


def catalog(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all().order_by('name')

    category_slug = request.GET.get('category')
    if category_slug:
        products = products.filter(category__slug=category_slug)

    context = {'products': products, 'categories': categories, 'products_count': products.count(), 'category_slug': category_slug}

    return render(
        request,
        'catalog.html',
        context
    )

# def category(request):
#     return render(request, 'category.html')