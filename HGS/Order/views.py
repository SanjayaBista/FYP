from django.shortcuts import render
from .models import ItemOrdered, Order
from .forms import OrderItemForm
from cart.cart import Cart
from Home.models import Category
# Create your views here.
def orderItem(request):
    category = Category.objects.all()
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                ItemOrdered.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            cart.clear()
            return render(request, 'orderSuccess.html', {'order':order, 'category':category})
        else:
            form = OrderItemForm()
        return render(request, 'checkout.html', {'cart':cart, 'form':form, 'category':category})