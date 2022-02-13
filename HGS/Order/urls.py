from django.urls import path
from .import views
app_name = 'order'

urlpatterns = [
    path('login/',views.userLogin,name='login'),
]
