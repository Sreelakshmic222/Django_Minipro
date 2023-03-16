from django.urls import path
from .views import Ddashboard
urlpatterns=[
    path('dashboardd/',Ddashboard.as_view(),name='dashboardd'),
    # path('orders/<int:pk>/',OdrderDetails.as_view(),name='order-details')

]