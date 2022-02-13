from django.urls import path
from .import views
app_name = 'cart'

urlpatterns = [
    path('login/',views.userLogin,name='login'),
]
