from django.contrib import admin
from .models import Customer, Address

# Register your models here.
@admin.register(Customer)
class AdminCustomer(admin.ModelAdmin):
    list_display = ['email','first_name','is_superuser','is_admin','is_staff','date_joined','last_login',]
    list_filter = ['date_joined','last_login',]
    search_fileds = ['email','first_name',]
    readonly_fields = ['id','date_joined','last_login',]    


@admin.register(Address)
class AdminAdderess(admin.ModelAdmin):
    list_display = ['city','state','district','postal','user','shippingAddress']
     
