from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def catalog(request):
    return render(request, 'catalog.html')

def wishlist(request):
    return render(request, 'wishlist.html')

def cart(request):
    return render(request, 'cart.html')