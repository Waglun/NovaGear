from django.http import JsonResponse
from django.shortcuts import render

def supplier_products(request):
    products = [
    {
        "sku": "RAZ-001",
        "name": "Razer DeathAdder V3",
        "price": 7990,
        "old_price": 8990,
        "description": "Эргономичная игровая мышь для динамичных игр.",
        "brand": "Razer",
        "category": "Gaming Mice",
        "stock": 15,
    },
    {
        "sku": "ASUS-001",
        "name": "ASUS ROG Strix Scope II",
        "price": 12990,
        "old_price": 14990,
        "description": "Механическая игровая клавиатура с подсветкой.",
        "brand": "ASUS",
        "category": "Keyboards",
        "stock": 8,
    },
]

    return JsonResponse(products, safe=False)
