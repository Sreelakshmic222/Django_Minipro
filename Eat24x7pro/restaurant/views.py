from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel
# Create your views here.
class Dashboard(View):
    def get(self,request,*args,**kwargs):
        #get the current date
        today=datetime.today()
        orders=OrderModel.objects.filter(created_on__year=today.year,created_on__month=today.month,created_on__day=today.day)
        #loop throught the orders and add the place value
        total_revenue=0
        for order in orders:
            total_revenue +=order.price
        #pass total number of orders and total revenue into template
        context={
            'orders':orders,
            'total_revenue':total_revenue,
            'total_orders':len(orders)
        }
        return render(request,'restaurant/dashboard.html',context)

class OrderDetails(View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)
        context={
            'order':order
        }
        return render(request,'restaurant/order-detail.html',context)

@login_required(login_url='rsignin')
def HomePage(request):
    return render(request, 'restaurant/dashboard.html')

def rsignup(request):
    if request.method == 'POST':

        email = request.POST.get('email')
        uname = request.POST.get('username')
        pass1 = request.POST.get('password')
        my_user = User.objects.create_user(uname, email, pass1)
        my_user.save()
        return redirect('rsignin')

    return render(request, 'restaurant/rsignup.html')
    # if request.method == 'POST':
    #     email = request.POST.get('email')
    #     username = request.POST['username']
    #     password = request.POST['password']
    #
    #
    #     myuser = User.objects.create_user(email,username,password)
    #
    #     myuser.save()
    #
    #     return redirect('rsignin')
    #
    # return render(request, 'restaurant/rsignup.html')

def rsignin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('rhome')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'restaurant/rsignin.html')
    # if request.method == 'POST':
    #     username = request.POST.get('username')
    #     password = request.POST.get('password')
    #     user = authenticate(request,username=username, password=password)
    #
    #     if user is not None:
    #         login(request, user)
    #         fname = user.username
    #         return render(request, 'restaurant/dashboard.html', {'fname': fname})
    #
    #     else:
    #         return redirect('rsignin')
    #
    # return render(request, 'restaurant/rsignin.html')

def LogoutPage(request):
    logout(request)
    return redirect('rsignin')