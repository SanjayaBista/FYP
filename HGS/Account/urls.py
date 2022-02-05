from django.urls import path
from .import views
app_name = 'account'

urlpatterns = [
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout'),
    path('register/',views.userRegister,name='register'),
    path('forgetPassword/',views.forgetPassword,name='forget'),
]
