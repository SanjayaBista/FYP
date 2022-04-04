from django.urls import path
from .import views
app_name = 'order'

urlpatterns = [
    path('orderItem/',views.orderItem,name='orderItem'),
    path('api/verify_payment/',views.verify_payment,name='verify_payment')
]
