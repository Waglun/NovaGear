from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from apps.catalog.models import Product
from .serializers import ProductSerializer, CartSerializer, CartItemSerializer, CartItemCreateSerializer, \
    ProductCreateSerializer


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
    search = request.query_params.get('search')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(sku__icontains=search)
        )

    result_page = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def product_create(request):
    serializer = ProductCreateSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.save()

        return Response(
            ProductSerializer(product).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart(request):
    cart = request.user.cart
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cart_item_create(request):
    cart = request.user.cart
    serializer = CartItemCreateSerializer(data=request.data)

    if serializer.is_valid():
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        if quantity > product.stock:
            return Response(
                {'detail': 'Недостаточно товара на складе.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item = cart.items.filter(product=product).first()
        if cart_item:
            cart_item.quantity = quantity
            cart_item.save(update_fields=['quantity'])
        else:
            cart_item = serializer.save(cart=cart)

        return Response(
            CartItemSerializer(cart_item).data,
            status=status.HTTP_201_CREATED
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)