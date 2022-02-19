from django.urls import path
from .import views
from .views import addCart, removeCart, detail
app_name = 'cart'

urlpatterns = [
    path('',views.detail,name='detail'),
    path('add/<int:product_id>/', views.addCart, name='addCart'),
    path('remove/<int:product_id>/',views.removeCart,name='cartRemove'),
]
