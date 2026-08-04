from .models import Product


class SessionCart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})

    def save(self):
        self.session.modified = True # Сообщение для Django что данные в сессии были изменены

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.save()

    def items(self):
        products = Product.objects.filter(id__in=self.cart.keys(), is_active=True)

        items = []
        for product in products:
            quantity = self.cart[str(product.id)]
            items.append(SessionCartItem(product, quantity))

        return items

    def total_price(self):
        return sum(item.subtotal_price for item in self.items())

    def total_item(self):
        total_item = sum(self.cart.values())
        return total_item

    def is_empty(self):
        return len(self.cart) == 0


class SessionCartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    @property
    def subtotal_price(self):
        return self.product.price * self.quantity

    @property
    def id(self):
        return self.product.id

    @property
    def price(self):
        return self.product.price