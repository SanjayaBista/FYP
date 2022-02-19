from django.shortcuts import render
from Home.models import Category, Product
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .cart import Cart
from .forms import AddProductForm
# Create your views here.

@login_required
def addCart(request, product_id):
    category = Category.objects.all()
    context = {'category':category}
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = AddProductForm(request.POST)
    if form.is_valid():
        data = form.cleaned_data
        cart.addItem(product=product,quantity=data['quantity'],override=data['override']) 
    return redirect('cart:detail',context)

@login_required
def removeCart(request, product_id):
    category = Category.objects.all()
    context = {'category':category}
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.removeItem(product)
    return redirect('cart:detail', context)

def detail(request):
    category = Category.objects.all()
    cart = Cart(request)
    context = {'cart':cart, 'category':category}
    return render(request, 'detail.html',context)