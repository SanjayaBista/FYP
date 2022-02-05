from unicodedata import category
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from .models import Category , Product

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
    context = {'category':category, 'product':product}
    return render(request, 'prodDetail.html',context)

