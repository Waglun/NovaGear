from .session import SessionCart
from .models import Cart


def cart_context(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        count = cart.total_item
    else:
        cart = SessionCart(request)
        count = cart.total_item()

    return {
        'cart_count': count,
    }