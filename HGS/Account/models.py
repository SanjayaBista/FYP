from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField(max_length=100,null=True)
    billing_address = models.TextField(max_length=100)
    zip_code = models.IntegerField()

    def __str__(self):
        return self.first_name