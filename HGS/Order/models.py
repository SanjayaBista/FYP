from django.db import models

from Home.models import Product, ProductAttribute
# Create your models here.

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

    class Meta:
        ordering = ('-orderedOn',)

    def __str__(self):
        return str(self.id)

    def total_cost(self):
        return sum(item.get_price() for item in self.items.all )

class ItemOrdered(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="itemOrder", on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)
    
    def get_price(self):
        return self.price * self.quantity