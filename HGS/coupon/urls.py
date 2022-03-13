from django.urls import path
from .import views

app_name = 'coupons'

urlpatterns = [
    path('useCoupon/', views.useCoupon, name = 'use')
]
