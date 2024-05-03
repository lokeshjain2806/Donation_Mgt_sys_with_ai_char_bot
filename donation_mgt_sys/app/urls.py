"""
URL configuration for donation_mgt_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from .views import Home, about, services, gallery, event, team, Login, Contact, Blog, RegistrationView, \
    Complete_Profile, OtpLogin, OtpFun, CustomPasswordResetView, UserLogout, login_view, Profile, PostDonaton, \
    CheckDonation, Chat_Bot
from django.contrib.auth.views import (
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', about, name='about'),
    path('services/', services, name='services'),
    path('gallery/', gallery, name='gallery'),
    path('event/', event, name='event'),
    path('team/', team, name='team'),
    path('sign_in/', Login.as_view(), name='login'),
    path('contact/', Contact.as_view(), name='contact'),
    path('blog/<int:id>/', Blog.as_view(), name='blogdetails'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('complete_profile/', Complete_Profile.as_view(), name='complete_profile'),
    path('otp_login/', OtpLogin.as_view(), name='otp_login'),
    path('otp_login/verification/', OtpFun.as_view(), name='otp_verification'),
    path('password-reset/', CustomPasswordResetView.as_view(template_name='resetpassword.html'),
         name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('home/', login_view, name='login_view'),
    path('home/profile/<int:pk>/', Profile.as_view(), name='profile'),
    path('home/post_donate/', PostDonaton.as_view(), name='post_donate'),
    path('home/check_donation/', CheckDonation.as_view(), name='check_donation'),
    path('home/chat_bot/', Chat_Bot.as_view(), name='chat_bot'),

]
