from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from .models import MenuItem, OrderModel,Category

"""Import Generic View Class"""


class Index(View):
    def get(selfself,request,*args,**kwargs):
        return render(request,'customer/index.html')

class About(View):
    def get(selfself,request,*args,**kwargs):
        return render(request,'customer/about.html')

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
        #Confirmation email after all completes
        body=('Thank Yoou for your Order! Your food is Coming\n'
              f'Your total:{price}\n'
              'Thank you again for your Order!')
        send_mail('Thank You For Your Order!',body,'example@example.com',
                  [email],
        )


        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)

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