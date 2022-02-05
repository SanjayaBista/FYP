from django.db import models
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
# Create your models here.

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
    # CATEGORY_CHOICE = (
    #     ('national','National'),
    #     ('international','International'),
    #     ('club','Club'),
    #     ('player','Player'),
    # )
    category = models.ForeignKey(Category,related_name='products', default='national',on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True, null=False )
    image = models.ImageField(blank=True)
    stock = models.IntegerField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    description = models.TextField(blank=True)
    availibility = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home:productDetail',args=[self.id, self.slug])