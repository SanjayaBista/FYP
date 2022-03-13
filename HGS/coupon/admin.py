from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class AdminCoupon(admin.ModelAdmin):
    list_display = ['code', 'startFrom', 'endOn', 'discount','active']
    list_filter = ['active', 'startFrom', 'endOn']
    search_fields = ['code']