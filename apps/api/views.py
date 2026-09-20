from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from apps.catalog.models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
def hello_api(request):
    message = {
            "message": "Hello from NovaGear API"
        }
    return Response(message)


@api_view(['GET'])
def products(request):
    paginator = PageNumberPagination()
    products = Product.objects.filter(is_active=True)
    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)