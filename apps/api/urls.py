from django.urls import path
from . import views

app_name = "api"

urlpatterns = [
    path('hello/', views.hello_api, name='hello'),
    path('products/', views.products, name='products'),
    path('product/<int:product_id>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('cart/items/', views.cart_item_create, name='cart_item_create'),
]
