from django.urls import path
from .views import Dashboard,OrderDetails,rsignup,rsignin
urlpatterns=[
    path('dashboard/',Dashboard.as_view(),name='dashboard'),
    path('orders/<int:pk>/',OrderDetails.as_view(),name='order-details'),
    path('rsignup/',rsignup,name='rsignup'),
    path('rsignin/',rsignin,name='rsignin'),

]