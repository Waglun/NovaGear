class SessionCart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.setdefault('cart', {})

    def save(self):
        self.session.modified = True