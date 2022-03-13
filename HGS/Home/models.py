from operator import mod
from re import T
from django.db import models
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from django.conf import settings

from Account.models import Customer
User = settings.AUTH_USER_MODEL
# Create your models here.

choices = {
    ''
}
class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length=200,null=False, unique=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_absolute_url(self):
        return reverse('home:categoryItem',args=[self.slug])

    def __str__(self):
        return self.name
    
    def __str__(self):                          
        full_path = [self.name]                 
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])


class Product(models.Model):
  
    category = models.ForeignKey(Category,related_name='products', default='national',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=False )
    image = models.ImageField(blank=True)
    image2 = models.ImageField(blank=True, null=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    title = models.CharField(max_length=100, null=True, blank=True)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(blank=True)
    long_description = models.TextField(blank=True, null=True)
    availibility = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
    # def get_category(self):
    #     return ",".join([str(p) for p in self.category.all()])

    def get_absolute_url(self):
        return reverse('home:productDetail',args=[self.id, self.slug])

class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='psize' , on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    availibility = models.BooleanField(default=True)

    def __str__(self):
        return self.title



class Comment(models.Model):
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    review = models.CharField(max_length=300, blank=True)
    rating = models.IntegerField(default=1)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.title

class Contact(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email  = models.EmailField()
    phoneNumber = models.CharField(max_length=10)
    message = models.TextField(max_length=300)
    