from .cart import Cart
def cart(request): #instantiate cart and available to all temp
    return {'cart':Cart(request)}