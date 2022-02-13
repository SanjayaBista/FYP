from unicodedata import name
from django.urls import path
from .import views
app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:id>/<slug:slug>/',views.categoryItem, name='categoryItem'),
    path('product/<int:id>/<slug:slug>/',views.productDetail, name='productDetail'),
    path('addComment/<int:id>',views.addComment,name='addComment'),
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('contactUs/',views.contactUs,name='contactUs'),
    path('condition/',views.conditon,name='condition'),
    path('exchange/',views.exchange,name='exchange'),
    path('shipping/',views.shipping,name='shipping'),

]
