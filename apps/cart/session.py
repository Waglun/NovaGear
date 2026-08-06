from .models import Product, CartItem, Cart


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

    def update(self, item_id, action):
        product_id = str(item_id)

        if product_id not in self.cart:
            return

        if action == 'increment':
            self.cart[product_id] += 1

        elif action == 'decrement':
            if self.cart[product_id] > 1:
                self.cart[product_id] -= 1
            else:
                del self.cart[product_id]

        self.save()

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
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

    def merge_to_database(self, user):
        print("=== MERGE START ===")
        cart, _ = Cart.objects.get_or_create(user=user)

        for item in self.items():
            cart_item, create = CartItem.objects.get_or_create(cart=cart, product=item.product, defaults={'quantity': item.quantity})

            if not create:
                cart_item.quantity += item.quantity
                cart_item.save(update_fields=['quantity'])

        self.cart.clear()
        self.save()


class SessionCartItem:
    def __init__(self, product, quantity):
        self.id = product.id
        self.product = product
        self.quantity = quantity

    @property
    def subtotal_price(self):
        return self.product.price * self.quantity

    @property
    def price(self):
        return self.product.price