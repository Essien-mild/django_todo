from . import views
from django.urls import path
from django.conf.urls import handler404


urlpatterns = [
   
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register_view, name="register"),
    path('verify/', views.verify_otp_view, name="verify_otp"),
    path('forgot_password/', views.forgot_password_view, name="forgot_password"),
    path('reset_password/', views.reset_password_view, name="reset_password"),  
    path('reset_password_verify/', views.reset_password_verify_view, name="reset_password_verify"),


             ]

