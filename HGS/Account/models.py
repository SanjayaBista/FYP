from unittest.mock import Base
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



class AccountManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, phone_number, password):
        if not email:
            raise ValueError("Email is necessary. ")
        if not username:
            raise ValueError("User Name is necessary.")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, first_name, last_name, phone_number, password):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number = phone_number,
        )
        user.is_admin = True
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


# Create your models here.
class Customer(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=100)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=200,null=True)
    last_name = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=10)

    date_joined = models.DateTimeField(verbose_name='date joined',auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = AccountManager()
   
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name','phone_number']

    def __str__(self):
        return str(self.first_name)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self,app_label):
        return True

class Address(models.Model):
    city = models.CharField(max_length=100, blank=True, null=True)
    shippingAddress = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    postal = models.TextField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)