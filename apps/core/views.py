from django.shortcuts import render

def home(request):
    print(f"=== HOME VIEW ===")
    print(f"Has session: {hasattr(request, 'session')}")
    if hasattr(request, 'session'):
        print(f"Session key: {request.session.session_key}")
        print(f"Session data: {dict(request.session)}")
    print(f"Cookies in request: {request.COOKIES}")
    return render(request, 'home.html')



def cart(request):
    return render(request, 'cart.html')