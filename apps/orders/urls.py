from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/payment/', views.payment, name='payment'),
    path('<int:order_id>/success/', views.payment_success, name='payment_success'),
    path('<int:order_id>/failed/', views.payment_failed, name='payment_failed'),
]
