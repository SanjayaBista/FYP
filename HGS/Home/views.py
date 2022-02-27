from ast import Pass
from email import message
from tkinter.tix import Form
from unicodedata import category
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from .forms import FormComment
from .models import Category, Contact , Product, Comment
from cart.forms import CartAddProductForm
# Create your views here.
def home(request):
    category = Category.objects.all()
    latest_product = Product.objects.all().order_by('-id')[:4]
    context = {'category':category, 'latest_product':latest_product}
    return render(request, 'home.html',context)

def categoryItem(request,id,slug=None):
    category = Category.objects.all()
    products = Product.objects.filter(category_id = id)
    context = {'category':category,'products':products}
    return render(request, 'national.html', context)

def productDetail(request,id,slug):
    category = Category.objects.all()
    product = Product.objects.get(pk = id)
    latest_product = Product.objects.all().order_by('-id')[:4]
    comment = Comment.objects.filter(product_id = id, active = True)
    cart_product_form = CartAddProductForm()
    context = {'category':category, 'product':product,'latest_product':latest_product, 'comment':comment,'cart_product_form':cart_product_form}
    return render(request, 'prodDetail.html',context)

def addComment(request,id):
    url = request.META.get('HTTP_REFERER')
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
            message.success(request,"Sent Successfully")
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

def shipping(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'shipping.html',context)