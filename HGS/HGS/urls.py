"""HGS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from unicodedata import name
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
 

urlpatterns = [
    
    path('admin/', admin.site.urls),\
    path('cart/', include('cart.urls', namespace='cart')),
    path('coupons/', include('coupon.urls', namespace='coupons')),
    path('',include('Home.urls',namespace='home')),
    path('accounts/', include('Account.urls',namespace='account')),
    path('orders/', include('Order.urls',namespace='orders')),
    path('accounts/', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"), name='password_reset'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"), name='password_reset_complete'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)