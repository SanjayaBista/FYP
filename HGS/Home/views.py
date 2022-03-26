from ast import Pass
from email import message
from itertools import count
from tkinter.tix import Form
from unicodedata import category
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .forms import FormComment
from .models import Category, Contact , Product, Comment, Wishlist
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .filters import ProdFilter
# Create your views here.
def home(request):
    category = Category.objects.all()
    latest_product = Product.objects.all().order_by('-id')[:4]
    count_item = Wishlist.objects.filter(user=request.user).count()
    cart_product_form = CartAddProductForm()
    context = {'category':category, 'latest_product':latest_product, 'cart_product_form':cart_product_form, 'count_item':count_item}
    return render(request, 'home.html',context)

#prodcut page
def categoryItem(request,id,slug=None):
    category = Category.objects.all()

    # ATOZID = request.GET.get('ATOZ')
    # print(ATOZID)
    sort_by = request.GET.get("sort", "l2h") 
    print(sort_by)
    if id:
        products = Product.objects.filter(category_id = id)
    elif sort_by == "l2h":
        products = Product.objects.filter(category_id = id).order_by('-name')
    elif sort_by == "h2l":
        products = Product.objects.filter(category_id = id).order_by('name')

# error in sorting and filtering
    # if id:
    #     products = Product.objects.filter(category_id = id)
    # elif ATOZID:
    #     products = Product.objects.filter(category_id = id).order_by('-name')
    # else:
    #     products = Product.objects.filter(category_id = id)

    context = {'category':category,'products':products}
    return render(request, 'national.html', context)

#detail page
def productDetail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk = id)
    latest_product = Product.objects.all().order_by('-id').exclude(id=id)[:4]
    count_item = Wishlist.objects.filter(user=request.user).count()
    comment = Comment.objects.filter(product_id = id, active = True)
    cart_product_form = CartAddProductForm()
    context = {'category':category, 'product':product,'latest_product':latest_product, 'comment':comment,'cart_product_form':cart_product_form, 'count_item':count_item}
    return render(request, 'prodDetail.html',context)

def addComment(request,id):
    url = request.META.get('HTTP_REFERER')
    form = FormComment
    if request.method == 'POST':
        form = FormComment(request.POST)
        if form.is_valid():
            data = Comment()
            data.title = form.cleaned_data['title']
            data.review = form.cleaned_data['review']  
            data.rating = form.cleaned_data['rating'] 
            data.product_id = id
            current_user = request.user
            data.user_id = current_user.id
            data.save()
            return HttpResponseRedirect(url)
        else:
            form = FormComment
    return HttpResponseRedirect(url)


# def addComment(request):
#     Pass

def aboutUs(request):
    category = Category.objects.all()
    context = {'category':category}

    return render(request,'about.html',context)

def contactUs(request):
    category = Category.objects.all()
    context = {'category':category}
   
    if request.method == "POST":
        contact = Contact()
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email  = request.POST.get('email')
        phoneNumber = request.POST.get('phone')
        message = request.POST.get('message')
        contact.firstName = firstName
        contact.lastName = lastName
        contact.email = email
        contact.phoneNumber = phoneNumber
        contact.message = message
        contact.save()
        return redirect ('home:contactUs')
        
    return render(request,'contact.html',context)

def conditon(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'condition.html',context)

def exchange(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'exchange.html',context)

def checkout(request):
    category = Category.objects.all()
    cart = Cart(request)
    context = {'category':category, 'cart':cart}
    return render(request,'checkout.html',context)

def shipping(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'shipping.html',context)

# def add_wishlist(request):
#     pid = request.GET['product']
#     return JsonResponse({'bool':True})

def add_wishlist(request):
    pid=request.GET['product']
    product = Product.objects.get(pk=pid)
    data={}
    checkWish=Wishlist.objects.filter(product=product,user=request.user).count()
    if checkWish > 0:
        data = {
            'bool':False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool':True
        }
    return JsonResponse(data)