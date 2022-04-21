from email import message
from weakref import ref
from django.conf import settings
import requests
import json 
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render
from .models import ItemOrdered, Order, Refund
from .forms import OrderItemForm
from cart.cart import Cart
from Home.models import Category, Product
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
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
            current_user = request.user
            order.user_id = current_user.id
            order.save()
            for item in cart:
                ItemOrdered.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                send_mail(
                        'Ordered Successfull',
                        'Thank you for Ordering. You will receive the product soon.',
                        settings.EMAIL_HOST_USER,
                        [request.user.email],
                        fail_silently=True,
                    )
            cart.clear()
            
            return render(request, 'orderSuccess.html', {'order':order, 'category':category})
    else:
        form = OrderItemForm()
    return render(request, 'checkout.html', {'cart':cart, 'form':form, 'category':category})

def refund(request,id):
    url = request.META.get('HTTP_REFERER')
    product = Product.objects.get(pk=id)
    refundOrd = ItemOrdered.objects.get(product=product, user=request.user)
    if request.method == "POST":
            refund = Refund()
            username = request.POST.get('username')
            refundOrder = request.POST.get('refundOrder')
            phone  = request.POST.get('phone')
            email = request.POST.get('email')
            reason = request.POST.get('reason')
            refund.username = username
            refund.refundOrder = refundOrder
            refund.phone = phone
            refund.email = email
            refund.reason = reason
            refund.save()
    return HttpResponseRedirect(url)


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

