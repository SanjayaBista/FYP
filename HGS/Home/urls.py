from django.urls import path
from .import views
app_name = 'home'

urlpatterns = [
    path('',views.home,name='home'),
    path('category/<int:id>/<slug:slug>/',views.categoryItem, name='categoryItem'),
    path('product/<int:id>/<slug:slug>/',views.productDetail, name='productDetail'),

]
