from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path('wishlist/', views.wishlist, name='wishlist'),
    path('cart/', views.cart, name='cart'),
]