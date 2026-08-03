from NovaGear.apps.catalog.models import Product


class SessionCart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})

    def save(self):
        self.session.modified = True # Сообщение для Django что данные в сессии были изменены

    def add(self, product_id, quantity=1):
        product_id = str(product_id)
        if product_id is self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.save()

    def items(self):
        products = Product.objects.filter(id__in=self.cart.keys(), is_active=True)

        items = []
        for product in products:
            quantity = self.cart[str(product.id)]
            items.append({
                'product_id': product.id,
                'quantity': quantity,
                'subtotal_price': product.price * quantity,
            })

        return items