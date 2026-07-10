from django.shortcuts import render

def catalog(request):
    return render(request, 'catalog.html')

# def category(request):
#     return render(request, 'category.html')