from django.contrib import admin
from .models import Order, ItemOrdered
# Register your models here.

class AdminOrderItem(admin.TabularInline):
    model = ItemOrdered
    raw_id_fields = ['product']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id','user', 'firstName', 'lastName', 'email','state','district','postalCode', 'address', 'orderedOn', 'moneyPaid']
    list_filter = ['moneyPaid', 'orderedOn']
    inlines = [AdminOrderItem]