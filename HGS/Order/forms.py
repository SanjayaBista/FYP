from django import forms
from .models import Order

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['firstName', 'lastName', 'email', 'state', 'district', 'postalCode','address']