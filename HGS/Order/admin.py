from django.contrib import admin
from .models import Order, ItemOrdered, Refund, RefundMsg
# Register your models here.

class AdminOrderItem(admin.TabularInline):
    model = ItemOrdered
    raw_id_fields = ['product']

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ['id','user', 'firstName', 'lastName', 'email','state','district','postalCode', 'address', 'orderedOn', 'moneyPaid']
    list_filter = ['moneyPaid', 'orderedOn']
    inlines = [AdminOrderItem]

# @admin.register(Refund)
# class AdminRefund(admin.ModelAdmin):
#     list_display = ['refundOrder','username','phone','email','reason']

@admin.register(RefundMsg)
class AdminRefund(admin.ModelAdmin):
    list_display = ['prodid','username','phone','email','reason']
  