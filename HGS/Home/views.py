from ast import Pass
import csv
from email import message
from itertools import count
from math import prod
from tkinter.tix import Form
from unicodedata import category
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .forms import FormComment, SearchQuery
from .models import Category, Contact , Product, Comment, ProductAttribute, Wishlist
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .filters import ProdFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.auth.decorators import login_required


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
    products = Product.objects.filter(category_id = id)

    ordering = request.GET.get('ordering',"")
    filtering = request.GET.get('filtering',"")
    if ordering:
        products = products.order_by(ordering)
    if filtering:
        products = products.filter(filtering)

    page_size_val = request.GET.get('page_size_val',2)
    paginator = Paginator(products, page_size_val)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    countProd = Product.objects.filter(category_id = id).count()

    context = {'category':category,'products':products,'page':page, 'countProd':countProd, 'allProd':allProd,'page_size_val':int(page_size_val)}
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
    count_item = Wishlist.objects.filter().count()
    comment = Comment.objects.filter(product_id = id, active = True)
    cart_product_form = CartAddProductForm()
   
    is_wishlist = False

    checkWish=Wishlist.objects.filter(product=product,user=request.user).count()
    if checkWish > 0:
        is_wishlist = True
    context = {'category':category, 'product':product,'latest_product':latest_product, 'comment':comment,'cart_product_form':cart_product_form, 'count_item':count_item,'is_wishlist':is_wishlist}
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

# def checkout(request):
#     category = Category.objects.all()
#     cart = Cart(request)
#     context = {'category':category, 'cart':cart}
#     return render(request,'checkout.html',context)

def shipping(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'shipping.html',context)

# def add_wishlist(request):
#     pid = request.GET['product']
#     return JsonResponse({'bool':True})


@login_required(login_url='account:login')
def add_wishlist(request, id):
    url = request.META.get('HTTP_REFERER')
    # pid=request.GET['product']
    product = Product.objects.get(pk=id)
    checkWish=Wishlist.objects.filter(product=product,user=request.user).count()
    if checkWish > 0:
        # prudct_id = 1 && user_id = 1
        wishlist = Wishlist.objects.get(product=product, user=request.user)
        wishlist.delete()
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
    
    return HttpResponseRedirect(url)

def remove_wishlist(request, product_id, wishlist_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = Wishlist.objects.get(product=product, user=request.user, id=wishlist_id)
    cart_item.delete()
    return redirect('wishlist')

    # product = Wishlist.objects.get(id=product_id, user=request.user)

    # product.delete()
    # return HttpResponseRedirect('/wishlist')

    # category = Category.objects.all()
    # cart = Cart(request)
    # product = get_object_or_404(Product, id=product_id)
    # cart.remove(product)
    # if cart:
    #     return redirect('cart:cart_detail')
    # return redirect('/', {'category':category}



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


def csvExport(request):
    rating = Comment.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=rating.csv'
    writer = csv.writer(response)
    writer.writerow(['User ID','Product ID','Rating'])
    ratingFields = rating.values_list('user_id','product_id','rating')
    for rate in ratingFields:
        writer.writerow(rate)
    return response

def csvExport2(request):
    product = Product.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=product.csv'
    writer = csv.writer(response)
    writer.writerow(['Product ID','Category ID','Price','Description'])
    productFields = product.values_list('id','category_id','price','description')
    for product in productFields:
        writer.writerow(product)
    return response


def csvExport3(request):
    size = ProductAttribute.objects.all()
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=size.csv'
    writer = csv.writer(response)
    writer.writerow(['Product ID','Size'])
    sizeFields = size.values_list('product_id','size_id')
    for size in sizeFields:
        writer.writerow(size)
    return response
