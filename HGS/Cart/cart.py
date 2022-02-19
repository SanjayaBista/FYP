from django.conf import settings
from Home.models import Product
from decimal import Decimal

class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def addItem(self, product, quantity=1, override_quantity = False):
        productID = str(product.id)
        if productID not in self.cart:
            self.cart[productID] = {'quantity':0, 'price':str(product.price)}
        
        if override_quantity:
            self.cart[productID]['quantity'] = quantity
        else:
            self.cart[productID]['quantity'] += quantity
        self.save()
    
    def removeItem(self, product):
        productID = str(product.id)
        if productID in self.cart:
            del self.cart[productID]
            self.save()
    
    def save(self):
        self.session.modified = True
    
    def __iter__(self):
        productIDs = self.cart.keys()
        products = Product.objects.filter(id__in=productIDs)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['totalPrice'] = item['price'] * item['quantity']
            yield product        
    
    def __len__(self):
        for item in self.cart.values():
            return sum(item['quantity'])
    
    def get_total_price(self):
        for item in self.cart.values():
            return sum(Decimal(item['price']) * item['quantity'])
    
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()