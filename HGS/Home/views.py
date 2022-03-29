from ast import Pass
from email import message
from itertools import count
from math import prod
from tkinter.tix import Form
from unicodedata import category
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .forms import FormComment, SearchQuery
from .models import Category, Contact , Product, Comment, Wishlist
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .filters import ProdFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.db.models import Q

# Create your views here.
def home(request):
    category = Category.objects.all()
    latest_product = Product.objects.all().order_by('-id')[:4]
    count_item = Wishlist.objects.filter().count()
    cart_product_form = CartAddProductForm()
    context = {'category':category, 'latest_product':latest_product, 'cart_product_form':cart_product_form, 'count_item':count_item}
    return render(request, 'home.html',context)

#prodcut page
def categoryItem(request,id,slug=None):
    category = Category.objects.all()
    allProd = Product.objects.all()
    ATOZID = request.GET.get('ATOZ')
    ZTOAID = request.GET.get('ZTOA')
    print(ATOZID)
    # print(ATOZID)
    # sort_by = request.GET.get('ATOZ') 
    # print(sort_by)
    # if id:
    #     products = Product.objects.filter(category_id = id)
    # elif sort_by == "l2h":
    #     products = Product.objects.filter(category_id = id).order_by('-name')
    # elif sort_by == "h2l":
    #     products = Product.objects.filter(category_id = id).order_by('name')

# error in sorting and filtering
    if id:
        products = Product.objects.filter(category_id = id)
    elif ATOZID:
        products = Product.objects.filter(category_id = id).order_by('-name')
       
    elif ZTOAID:
        products = Product.objects.filter(category_id = id).order_by('name')
    else:
        products = Product.objects.filter(category_id = id)
    paginator = Paginator(products, 4)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    countProd = Product.objects.filter(category_id = id).count()

    context = {'category':category,'products':products,'page':page, 'countProd':countProd, 'allProd':allProd}
    return render(request, 'national.html', context)

# def findProd(request):
#     chosenProd = None
#     products = Product.objects.all()
#     if request.method == 'POST':
#         chosenProd = request.POST.get('product')
#         produts = products.filter(product=chosenProd)
        




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


# def search(arr, x):
#     products = Product.objects.values_list('name',flat=True)
#     products = list(products)
#     l = 0
#     r = len(arr)
#     while (l <= r):
#         m = l + ((r - l) // 2)
 
#         res = (x == arr[m])
 
#         # Check if x is present at mid
#         if (res == 0):
#             return m - 1
 
#         # If x greater, ignore left half
#         if (res > 0):
#             l = m + 1
 
#         # If x is smaller, ignore right half
#         else:
#             r = m - 1
 
#     return -1
 

def prodSearch(request):
    category = Category.objects.all()
    if request.method=='POST':
        search = request.POST.get('search')
        results = Product.objects.filter(Q(name__icontains=search))
        context = {'category':category, 'results': results}
        return render(request, 'search.html', context)
    else:
        return redirect('home:home')
