from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Customer , Address
from .forms import RegisterForm
from Home.models import Category, Wishlist
from django.contrib import messages
# Create your views here.
def userLogin(request):
    category = Category.objects.all()
    context = {'category':category}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home:home')
        else:
            messages.error(request, "Incorrect Username or Password ")

    return render(request,'login.html',context)

def userLogout(request):
    logout(request)
    return  redirect('home:home')


def userRegister(request):
    category = Category.objects.all()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            first_name = user_form.cleaned_data['first_name']
            last_name = user_form.cleaned_data['last_name']
            email = user_form.cleaned_data['email']
            phone_number = user_form.cleaned_data['phone_number']
            password = user_form.cleaned_data['password']
            username = user_form.cleaned_data['username']
            customer = Customer.objects.create_user(first_name=first_name,last_name=last_name,email=email,phone_number=phone_number,password=password,username = username)
            customer.save()
            return redirect('account:login')
        else:
            messages.error(request, "Password did not match. ")
    else:
        user_form = RegisterForm()
    context = {'user_form':user_form,'category':category}
    return render(request,'accountCreate.html',context)

def forgetPassword(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'resetpassword.html',context)

def profile(request):
    category = Category.objects.all()
    context = {'category':category}
   
    return render(request,'profile.html',context)

def updateProfile(request):
    category = Category.objects.all()
    context = {'category':category}
    if request.method=='POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        phoneNumber = request.POST['phoneNumber']
        customer = Customer.objects.get(id=request.user.id)
        customer.first_name = firstName
        customer.last_name = lastName
        customer.email = email
        customer.phone_number = phoneNumber
        customer.save()
    return render(request, 'profile.html', context)

def address(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'myaddress.html',context)

def updateAddress(request):
    category = Category.objects.all()
    context = {'category':category, 'info':info}
    if request.method=="POST":
        info = Address()
        state = request.POST.get('state')
        district = request.POST.get('district')
        address = request.POST.get('address')
        postal  = request.POST.get('zip')
        info.state = state
        info.district = district
        info.address = address
        info.postal = postal
        current_user = request.user
        info.user_id = current_user.id
        info.save()
        return redirect('account:address')

    return render (request, 'myaddress.html', context)
def wishlist(request):
    category = Category.objects.all()
    wish = Wishlist.objects.filter(user=request.user).order_by('-id')
    count_item = Wishlist.objects.filter(user=request.user).count()
    context = {'category':category,'wish':wish, 'count_item':count_item}
    return render(request,'wishlist.html',context)

def history(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'history.html',context)