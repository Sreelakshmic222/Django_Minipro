from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.timezone import datetime
from customer.models import OrderModel

# Create your views here.
@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
            return redirect('dsignin')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('dhome')
        else:
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('dsignin')

class Dashboard(View):
    def get(self,request,*args,**kwargs):
        #get the current date
        today=datetime.today()
        orders=OrderModel.objects.filter(created_on__year=today.year,created_on__month=today.month,created_on__day=today.day)
        #loop throught the orders and add the place value
        # total_revenue=0
        # for order in orders:
        #     total_revenue +=order.price
        #pass total number of orders and total revenue into template
        context={
            'orders':orders,
            # 'total_revenue':total_revenue,
            'total_orders':len(orders)
        }
        return render(request,'restaurant/dashboard.html',context)