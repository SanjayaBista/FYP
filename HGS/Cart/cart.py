from django.conf import settings
from Home.models import Product
from decimal import Decimal
from coupon.models import Coupon
class Cart(object):
    def __init__(self,request):
        self.session = request.session #store current session
        cart = self.session.get(settings.CART_SESSION_ID) #get cart from the current session
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {} #empty cart session
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id') #get coupon in the session
# ,is_customize=False
    def add(self,product,quantity=1,override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity':0, 'price':str(product.price)} #store in the cart
        # if int(is_customize) == 1:
        #     self.cart[product_id] ['is_customize'] = True
        if override_quantity:
            self.cart[product_id] ['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity #increase quantity
        self.save()
    
    def save(self):
        self.session.modified = True #modified cart session save
    
    def remove(self,product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def __iter__(self):
        product_ids = self.cart.keys() #get prod from db
        products = Product.objects.filter(id__in=product_ids) #add prod obj to cart
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)] ['product'] = product
        
        for item in cart.values():
            # if item['is_customize'] == True:
            #     item['price'] = Decimal(item['price']) + 100
            # else:
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item 
    
    def __len__(self): #retrieves total items in cart
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self): #total cost in cart
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def clear(self): #removes cart session
        del self.session[settings.CART_SESSION_ID]
    
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    
    def get_discount(self):
        if self.coupon:
            return(self.coupon.discount / Decimal(100) * self.get_total_price())
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount() 