from django.shortcuts import render, redirect, get_object_or_404
from coupon.forms import CouponForm
from Home.models import Product, Category
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='account:login')
def cart_add(request, product_id):
    # category = Category.objects.all()
    # context = {'category':category}
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,quantity=cd['quantity'],override_quantity=cd['override'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    category = Category.objects.all()
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    if cart:
        return redirect('cart:cart_detail')
    return redirect('/', {'category':category})

def cart_detail(request):
    category = Category.objects.all()
    latest_product = Product.objects.all().order_by('-id')[:5]
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity':item['quantity'],
            'override':True
        })
    coupon_apply_form = CouponForm()
    return render(request,'cart/detail.html',{'cart':cart,'category':category, 'latest_product':latest_product, 'coupon_apply_form':coupon_apply_form})
