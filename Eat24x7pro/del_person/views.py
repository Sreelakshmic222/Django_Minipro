from django.shortcuts import render
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel
# Create your views here.
class Ddashboard(View):
    def get(self,request):
        return render(request,"del_person/dashboard.html")
#
#
# class OdrderDetails(View):
#     def get(self,request,pk,*args,**kwargs):
#         order=OrderModel.objects.get(pk=pk)
#         context={
#             'order':order
#         }
#         return render(request,'del_person/order-details.html',context)
#
#
