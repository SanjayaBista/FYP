from django.conf import settings
from django.db import models
from Account.models import Customer
from Home.models import Product, ProductAttribute
# Create your models here.
User = settings.AUTH_USER_MODEL

class Order(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField()
    state = models.CharField(max_length=100)
    district =models.CharField(max_length=100)
    postalCode = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    orderedOn = models.DateTimeField(auto_now_add=True)
    moneyPaid = models.BooleanField(default=False)
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    class Meta:
        ordering = ('-orderedOn',)

    def __str__(self):
        return str(self.id)

    def total_cost(self):
        return sum([item.get_price() for item in self.items.all()] )

class ItemOrdered(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="itemOrder", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_price(self):
        return self.price * self.quantity

class Refund(models.Model):
    refundOrder = models.ForeignKey(ItemOrdered, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    reason = models.CharField(max_length=500)

    def __str__(self):
        return str(self.id)

class RefundMsg(models.Model):
    username = models.CharField(max_length=100,blank=False,null=False)
    phone = models.CharField(max_length=100,blank=False,null=False)
    email = models.CharField(max_length=100,blank=False,null=False)
    reason = models.CharField(max_length=100,blank=False,null=False)
    prodid = models.CharField(max_length=100,blank=False,null=False)

    def __str__(self):
        return str(self.id)