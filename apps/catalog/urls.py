from django.urls import path
from . import views

app_name = "catalog"

urlpatterns = [
    path('category/<slug:cat_slug>/', views.category, name='category'),
]

