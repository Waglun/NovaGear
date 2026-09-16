from django.http import JsonResponse
from django.shortcuts import render

def supplier_products(request):
    products = [
    {
        "sku": "RAZ-001",
        "name": "Razer DeathAdder V3",
        "price": 5990,
        "old_price": 7990,
        "description": "Эргономичная игровая мышь для динамичных игр.",
        "brand": "Razer",
        "category": "Gaming Mice",
        "stock": 12,
    },
    {
        "sku": "ASUS-001",
        "name": "ASUS ROG Strix Scope II",
        "price": 11990,
        "old_price": 12990,
        "description": "Механическая игровая клавиатура с подсветкой.",
        "brand": "ASUS",
        "category": "Keyboards",
        "stock": 8,
    },
]

    return JsonResponse(products, safe=False)
