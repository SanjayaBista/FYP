from django.db import models

# Create your models here.

class Category(models.Model):
    categoryID = models.IntegerField(primary_key=True)
    categoryName = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200,unique=True)

    class Meta:
        verbose_name = 'category'   
        verbose_name_plural = "categories"

    def __str__(self):
        return self.categoryName

class Product(models.Model):
    CATEGORY_CHOICE = (
        ('national','National'),
        ('international','International'),
        ('club','Club'),
        ('player','Player'),
    )
    productID = models.IntegerField(primary_key=True)
    categoryID = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    categoryName = models.CharField(max_length=15, choices=CATEGORY_CHOICE, default='national')
    productName = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
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
        return self.categoryName
