from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .import views
app_name = 'account'

urlpatterns = [
    path('login/',views.userLogin,name='login'),
    path('logout/',views.userLogout,name='logout'),
    path('register/',views.userRegister,name='register'),
    path('profile/',views.profile,name='profile'),
    path('updateProfile/',views.updateProfile,name='updateProfile'),
    path('address/',views.address,name='address'),
    path('updateAddress/',views.updateAddress,name='updateAddress'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('history/',views.history,name='history'),
    path('historyDetail/',views.historyDetail,name='historyDetail'),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),

    


    # path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"), name="password_reset_done"),
    # path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),

]
