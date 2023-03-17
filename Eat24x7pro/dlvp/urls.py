from django.urls import path
from  dlvp.views import Dash

urlpatterns=[
path('dash/',Dash.as_view(),name='dash'),

]
