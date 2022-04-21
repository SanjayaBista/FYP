from unicodedata import name
from django.urls import path
from .import views
app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('add_wishlist/<int:id>/',views.add_wishlist, name='add_wishlist'),
    path('remove_wishlist',views.remove_wishlist, name='remove_wishlist'),
    path('category/<int:id>/<slug:slug>/',views.categoryItem, name='categoryItem'),
    path('product/<int:id>/<slug:slug>/',views.productDetail, name='productDetail'),
    path('customize/<int:id>',views.customize,name='customize'),
    path('addComment/<int:id>',views.addComment,name='addComment'),
    path('aboutUs/',views.aboutUs,name='aboutUs'),
    path('contactUs/',views.contactUs,name='contactUs'),
    path('condition/',views.conditon,name='condition'),
    path('exchange/',views.exchange,name='exchange'),
    path('shipping/',views.shipping,name='shipping'),
    path('search/',views.prodSearch, name='search'),
    # path('csvExport/',views.csvExport, name='csvExport'),
    # path('csvExport2/',views.csvExport2, name='csvExport2'),
    # path('csvExport3/',views.csvExport3, name='csvExport3'),
    path('csvExport4/',views.csvExport4, name='csvExport4'),
]
