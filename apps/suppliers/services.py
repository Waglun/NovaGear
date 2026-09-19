import requests
from apps.catalog.models import Brand
from apps.catalog.models import Category
from apps.catalog.models import Product
from django.utils.text import slugify


def get_supplier_products():
    url = 'http://127.0.0.1:8000/suppliers/products/'
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as error:
        print(f'Ошибка запроса к API поставщика: {error}')
        return []

    except ValueError as error:
        print(f'Ошибка обработки JSON: {error}')
        return []


def import_supplier_products():
    products = get_supplier_products()

    for product_data in products:
        brand = Brand.objects.get(name=product_data['brand'])
        category = Category.objects.get(name=product_data['category'])

        product, created = Product.objects.update_or_create(
            sku=product_data['sku'],
            defaults={
                'name': product_data['name'],
                'price': product_data['price'],
                'old_price': product_data['old_price'],
                'description': product_data['description'],
                'brand': brand,
                'category': category,
                'stock': product_data['stock'],
                'slug': slugify(product_data['name'])
            }
        )

        print(product, created)


def update_supplier_products():
    products = get_supplier_products()

    for product_data in products:
        try:
            product = Product.objects.get(sku=product_data['sku'])

            product.price = product_data['price']
            product.old_price = product_data['old_price']
            product.stock = product_data['stock']

            product.save(update_fields=['price', 'stock', 'old_price'])

            print(product, product.price, product.stock)
        except Product.DoesNotExist:
            print(f"Товар с SKU {product_data['sku']} не найден в NovaGear")