"""food_pandas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from accounts import views
from django.views.generic import RedirectView

urlpatterns = [
    path('register/',views.register,name='register'),
    path('activate/<uidb64>/<token>/',views.activate_account,name='activate'),
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),
    path('profile/',views.profile,name='accounts_settings'),
    #Password reset
    path('password_reset/',views.password_reset,name='password_reset'),
    path('password_activate/<uidb64>/<token>',views.password_activate_account,name='password_activate'),
    path('changeYour_password/<str:user>',views.change_password,name='change_password'),
    path('',RedirectView.as_view(url='register/'))
]
