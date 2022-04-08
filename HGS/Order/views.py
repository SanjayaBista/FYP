from email import message
import requests
import json 
from django.contrib import messages
from django.http import JsonResponse

from django.shortcuts import render
from .models import ItemOrdered, Order
from .forms import OrderItemForm
from cart.cart import Cart
from Home.models import Category
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def orderItem(request):
    category = Category.objects.all()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                ItemOrdered.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'orderSuccess.html', {'order':order, 'category':category})
    else:
        form = OrderItemForm()
    return render(request, 'checkout.html', {'cart':cart, 'form':form, 'category':category})

@csrf_exempt
def verify_payment(request):
    data = request.POST
    product_id = data['product_identity']
    token = data['token']
    amount = data['amount']

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {
    "token": token,
    "amount": amount
    }
    headers = {
    "Authorization": "Key test_secret_key_7a19aba555514506ab3f9e50086e1c23"
    }
   
    response = requests.post(url, payload, headers = headers)
    response_data = response.json()
    status_code = str(response.status_code)  

    if status_code == '400':
        response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
        return response

    import pprint 
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(response_data)
    # return render(request,messages.error(request, "Payment Success"))
    return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)