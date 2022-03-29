from django.urls import path
from .import views
app_name = 'account'

urlpatterns = [
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout'),
    path('register/',views.userRegister,name='register'),
    path('forgetPassword/',views.forgetPassword,name='forgot'),
    path('profile/',views.profile,name='profile'),
    path('updateProfile/',views.updateProfile,name='updateProfile'),
    path('address/',views.address,name='address'),
    path('updateAddress/',views.updateAddress,name='updateAddress'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('history/',views.history,name='history'),
]
