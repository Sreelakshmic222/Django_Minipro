from django.urls import path
from .views import SignupPage,LoginPage,LogoutPage,HomePage
urlpatterns=[
    path('dhome/',HomePage,name='dhome'),
    path('dsignup/',SignupPage,name='dsignup'),
    path('dsignin/',LoginPage,name='dsignin'),
    path('dlogout/',LogoutPage,name='dlogout'),


]