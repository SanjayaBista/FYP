from email import message
from weakref import ref
from django.conf import settings
import requests
import json 
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse

from django.shortcuts import render
from .models import ItemOrdered, Order, Refund, RefundMsg
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
            order.moneyPaid = True
            order.save()
            for item in cart:
                ItemOrdered.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                newItem =Product.objects.filter(id=item['product'].id).first()
                newItem.stock = newItem.stock - item['quantity']
                newItem.save()
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

# def refund(request):
#     url = request.META.get('HTTP_REFERER')
    # refundOrd = ItemOrdered.objects.get(user=request.user)
    # if request.method == "POST":
    #         refund = Refund()
    #         username = request.POST.get('username')
    #         refundOrder = request.POST.get('refundOrder')
    #         phone  = request.POST.get('phone')
    #         email = request.POST.get('email')
    #         reason = request.POST.get('reason')
    #         refund.username = username
    #         refund.refundOrder = refundOrder
    #         refund.phone = phone
    #         refund.email = email
    #         refund.reason = reason
    #         refund.save()
    # return HttpResponseRedirect(url)


    # category = Category.objects.all()
    # context = {'category':category}

    # if request.method == "POST":
    #     refund = Refund()
    #     username = request.POST.get('username')
    #     id = request.POST.get('id')
    #     phone  = request.POST.get('phone')
    #     email = request.POST.get('email')
    #     reason = request.POST.get('reason')
    #     refund.username = username
    #     refund.id = id
    #     refund.phone = phone
    #     refund.email = email
    #     refund.reason = reason
    #     refund.product_id = id
    #     current_user = request.user
    #     refund.user_id = current_user.id
    #     refund.save()
    #     messages.error(request, "Refund Message Sent Successfully ")
    #     return HttpResponseRedirect(url)
        
def refundMsg(request):
    url = request.META.get('HTTP_REFERER')
    category = Category.objects.all()
    context = {'category':category}

    if request.method == "POST":
        refund = RefundMsg()
        username = request.POST.get('username')
        prodid = request.POST.get('prodid')
        phone  = request.POST.get('phone')
        email = request.POST.get('email')
        reason = request.POST.get('reason')
        refund.username = username
        refund.prodid = prodid
        refund.phone = phone
        refund.email = email
        refund.reason = reason
        current_user = request.user
        refund.user_id = current_user.id
        refund.save()
        messages.error(request, "Refund Message Sent Successfully. We will contact soon on email. ")
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
    "Authorization": "Key test_secret_key_db52a363f99b45108f229ebdf7e93de1"
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
    return JsonResponse(f"Payment Done. {response_data['user']['idx']}",safe=False)

