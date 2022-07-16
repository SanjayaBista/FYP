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
from django.contrib import messages
from Home.recommender import getRecommendation
from .forms import FormComment, SearchQuery
from .models import Category, Contact, Customize , Product, Comment, ProductAttribute, Wishlist
from cart.forms import CartAddProductForm
from cart.cart import Cart
from .filters import ProdFilter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from PIL import Image , ImageDraw, ImageFont

# Create your views here.
def home(request):
    category = Category.objects.all()
    latest_product = Product.objects.all().order_by('-id')[:4]
    for i in latest_product:
        is_wishlist = False
        if request.user.is_authenticated:
            checkWish=Wishlist.objects.filter(product=i,user=request.user).count()
            if checkWish > 0:
                is_wishlist = True
        i.is_wishlist = is_wishlist    
    count_item = Wishlist.objects.filter().count()
    cart_product_form = CartAddProductForm()
    context = {'category':category, 'latest_product':latest_product, 'cart_product_form':cart_product_form, 'count_item':count_item}
    return render(request, 'home.html',context)

#prodcut page
def categoryItem(request,id,slug=None):
    category = Category.objects.all()
    allProd = Product.objects.all()
    products = Product.objects.filter(category_id = id)
    for i in products:
        is_wishlist = False
        if request.user.is_authenticated:
            checkWish=Wishlist.objects.filter(product=i,user=request.user).count()
            if checkWish > 0:
                is_wishlist = True
        i.is_wishlist = is_wishlist    
    ordering = request.GET.get('ordering',"")
    filtering = request.GET.get('filtering',"")
    if ordering:
        products = products.order_by(ordering)
    if filtering:
        products = products.filter(filtering)
    page_size_val = request.GET.get('page_size_val',4)
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
  
    count_item = Wishlist.objects.filter().count()
    comment = Comment.objects.filter(product_id = id, active = True)
    cart_product_form = CartAddProductForm()
   
    is_wishlist = False
    if request.user.is_authenticated:
        checkWish=Wishlist.objects.filter(product=product,user=request.user).count()
        if checkWish > 0:
            is_wishlist = True
    prodIds = getRecommendation(id)
    recommProd = []
    for i in range(0, len(prodIds)):
        recommProd.append(Product.objects.get(id = prodIds[i]))
    context = {'category':category, 'product':product,'recommProd':recommProd, 'comment':comment,'cart_product_form':cart_product_form, 'count_item':count_item,'is_wishlist':is_wishlist}
    return render(request, 'prodDetail.html',context)


def customize(request,id):
    url = request.META.get('HTTP_REFERER')
    category = Category.objects.all()
    product = Product.objects.get(pk = id)
    img = Image.open(product.image2)
    d = ImageDraw.Draw(img)
    fnt = ImageFont.truetype("comicbd.ttf",100)
    if request.method == "POST":
        customize = Customize()
        name = request.POST.get('name')
        number = request.POST.get('number')
        customize.name = name
        customize.number = number
        customize.product_id = id
        current_user = request.user
        customize.user_id = current_user.id
        customize.save()
    # name = request.POST.get('name')
    # number = request.POST.get('number')
    d.text((230,100),name,font=fnt,fill=(255,255,255))
    d.text((320,230),number,font=fnt,fill=(255,255,255))
    img.save('a.png')
    image_path = 'C:/Users/DeLL/Desktop/CodingFYP/HGS/a.png'
    img = Image.open(image_path)
    img.save('static/b.png')
    # print(img.path,'-------------------------')
   
    return JsonResponse({'status':'success'})
    # return HttpResponseRedirect(url, context)


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
        messages.error(request, "Message Sent Successfully ")
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


# def csvExport(request):
#     rating = Comment.objects.all()
#     response = HttpResponse('text/csv')
#     response['Content-Disposition'] = 'attachment; filename=rating.csv'
#     writer = csv.writer(response)
#     writer.writerow(['User ID','Product ID','Rating'])
#     ratingFields = rating.values_list('user_id','product_id','rating')
#     for rate in ratingFields:
#         writer.writerow(rate)
#     return response

# def csvExport2(request):
#     product = Product.objects.all()
#     response = HttpResponse('text/csv')
#     response['Content-Disposition'] = 'attachment; filename=product.csv'
#     writer = csv.writer(response)
#     writer.writerow(['Product ID','Category ID','Price','Description'])
#     productFields = product.values_list('id','category_id','price','description')
#     for product in productFields:
#         writer.writerow(product)
#     return response


# def csvExport3(request):
#     size = ProductAttribute.objects.all()
#     response = HttpResponse('text/csv')
#     response['Content-Disposition'] = 'attachment; filename=size.csv'
#     writer = csv.writer(response)
#     writer.writerow(['Product ID','Size'])
#     sizeFields = size.values_list('product_id','size_id')
#     for size in sizeFields:
#         writer.writerow(size)
#     return response

def csvExport4(request):
    rating = Comment.objects.all()
    size = ProductAttribute.objects.all()
    product = Product.objects.all()
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename=rating.csv'
    writer = csv.writer(response)
    writer.writerow(['id','Price','Description','Rating','Size'])
    ratingFields = rating.values_list('rating')
    sizeFields = size.values_list('size_id')
    productFields = product.values_list('id','price','description')
    product_list = []
    rate_list = []
    size_list = []
    for product in productFields:
        product_list.append(product)
    for rate in ratingFields:
        rate_list.append(rate)
    for size in sizeFields:
        size_list.append(size)
    for i in range(0,len(product_list)):
        writer.writerow( product_list[i] + rate_list[i] + size_list[i])
    return response

