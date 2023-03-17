from django.shortcuts import render
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel
# Create your views here.
class Dash(View):
    def get(self,request,*args,**kwargs):
        return render(request,'dlvp/dash.html')




