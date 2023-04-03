from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.fields import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from .models import MenuItem, OrderModel,Category
from Eat24x7pro import settings

"""Import Generic View Class"""

def mail(request):
    subject="Order Placed Successfully"
    msg="Thank You For Your Order! Visit Again"
    to="sreelakshmic222@gmail.com"
    res=send_mail(subject,msg,settings.EMAIL_HOST_USER,[to])
    if res==1:
        msg="Mail sent Successfully"
    else:
        msg="Mail could not sent"
    return HttpResponse(msg)


class Index(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/Home.html')

class About(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/about.html')
class Pricing(View):
    def get(self,request,*args,**kwargs):
        return render(request,'customer/pricing.html')

class Order(View):
    def get(self,request,*args,**kwargs):
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POST.get('name')
        email=request.POST.get('email')
        street=request.POST.get('street')
        city= request.POST.get('city')
        state=request.POST.get('state')
        zip_code=request.POST.get('zip_code')


        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(price=price,name=name,email=email,street=street,city=city,state=state,zip_code=zip_code)
        order.items.add(*item_ids)

        context = {
            'items': order_items['items'],
            'price': price
        }
        return redirect('order-confirmation',pk=order.pk)
        # return render(request, 'customer/order_confirmation.html', context)

class OrderConfirmation(View):
    def get(self,request,pk,*args,**kwargs):
        order=OrderModel.objects.get(pk=pk)

        context={
            'pk':order.pk,
            'items':order.items,
            'price':order.price
        }
        return render(request,'customer/order_confirmation.html',context)

    def post(self,request,pk,*args,**kwargs):
        data=json.loads(request.body)

        if data['isPaid']:
            order=OrderModel.objects.get(pk=pk)
            order.is_paid=True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')






def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username, email, pass1)

        myuser.save()

        return redirect('signin')

    return render(request, 'customer/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.username
            return render(request, 'customer/base.html', {'fname': fname})

        else:
            return redirect('signin')

    return render(request, 'customer/signin.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully!')
    return redirect('signin')

def home(request):
    template="customer/Home.html"
    context={}
    return render(request,template,context)

class Menu(View):
    def get(self,request,*args,**kwargs):
        menu_items = MenuItem.objects.all()

        context = {
            'menu_items':menu_items
        }
        return render(request,'customer/menu.html',context)

class MenuSearch(View):
    def get(self,request,*args,**kwargs):
        query=self.request.GET.get("q")

        menu_items=MenuItem.objects.filter(
            Q(name__icontains=query) |
            Q(price__icontains=query)|
            Q(description__icontains=query)
        )

        context={
            'menu_items':menu_items
        }
        return render(request,'customer/menu.html',context)