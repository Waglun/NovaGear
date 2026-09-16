from django.urls import path
from . import views


app_name = 'suppliers'

urlpatterns = [
    path('products/', views.supplier_products, name='suppliers'),
]