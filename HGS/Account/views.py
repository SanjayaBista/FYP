from multiprocessing import context
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .models import Customer
from .forms import RegisterForm
from Home.models import Category
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

    return render(request,'login.html',context)

def userLogout(request):
    logout(request)
    return  redirect('home:home')

def userRegister(request):
    category = Category.objects.all()
    context = {'category':category}
    if request.method == 'POST':
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        email = request.POST['email']
        phoneNumber = request.POST['phoneNumber']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        customer = Customer.objects.create(firstName=firstName,lastName =lastName,email =email,phone =phoneNumber,password=password,confirmPassword=confirmPassword)
        customer.save()
        return redirect('home:home')
    else:
     return render(request, 'accountCreate.html',context)


# def userRegister(request):
#     if request.method == 'POST':
#         user_form = RegisterForm(request.POST)
#         if user_form.is_valid():
#             #creates new user object but doesnt save yet
#             new_user = user_form.save(commit=False)
#             #set chosen password
#             new_user.set_password(user_form.cleaned_data['password'])
#             #save user object
#             new_user.save()
#             #create the user Profile
#             Customer.objects.create(user=new_user)
#             return render(request,'home:home',{'new_user':new_user})
#     else:
#         user_form = RegisterForm()
#     return render(request,'accountCreate.html',{'user_form':user_form})



# class RegisterView(CreateView):
#     template_name = "accountCreate.html"
#     form_class = RegisterForm
#     success_url = reverse_lazy('"home:home"')

def forgetPassword(request):
    return render(request,'resetpassword.html')