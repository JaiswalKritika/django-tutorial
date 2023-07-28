from django.http import HttpResponse
from django.template import loader
from .models import *
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Min,Max
def members(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/homepage2.html')
  return HttpResponse(template.render())

def homepage(request):
  product=Products.objects.filter(status='PUBLISH')
  category=Categories.objects.filter(status='PUBLISH')
  Category_id = request.GET.get('category')



  context={
      'product':product,'category':category,
  }

  return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/header2.html', context)



@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = get_object_or_404(Products, id=product_id)

    # Check whether the Product is alread in Cart or Not
    item_already_in_cart = Cart.objects.filter(product=product_id, user=user)
    if item_already_in_cart:
        cp = get_object_or_404(Cart, product=product_id, user=user)
        cp.quantity += 1
        cp.save()
    else:
        Cart(user=user, product=product).save()

    return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/cart.html')



def cart(request):

    return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/cart.html')


@login_required
def remove_cart(request, cart_id):
    if request.method == 'POST':
        c = get_object_or_404(Cart, id=cart_id)
        c.delete()
        messages.success(request, "Product removed from Cart.")
    return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/cart.html')


@login_required
def plus_cart(request, cart_id):
    if request.method == 'POST':
        cp = get_object_or_404(Cart, id=cart_id)
        cp.quantity += 1
        cp.save()
    return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/cart.html')


@login_required
def minus_cart(request, cart_id):
    if request.method == 'POST':
        cp = get_object_or_404(Cart, id=cart_id)
        # Remove the Product if the quantity is already 1
        if cp.quantity == 1:
            cp.delete()
        else:
            cp.quantity -= 1
            cp.save()
    return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/cart.html')


def checkout(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/checkout.html')
  return HttpResponse(template.render())


def order_complete(request):

    return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/order_complete.html')





def register(request):
  if request.method == "POST":
    first_name = request.POST["first_name"]
    last_name = request.POST["last_name"]
    email = request.POST["email"]
    mobile = request.POST["mobile"]
    password = request.POST["password"]
    user_obj=User.objects.filter(username=email)
    if user_obj.exists():
        context = {'message': 'Email is already taken.', 'class': 'danger'}
        return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/register.html', context)
    user_obj=User.objects.create(first_name=first_name,last_name=last_name,email=email,username=email)
    user_obj.set_password(password)
    user_obj.save()
    print(email)
    context = {'message': ' An Email has been sent on your email.', 'class': 'success'}
    return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/register.html',   context)


  return render(request, "cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/register.html")

def activate_email(request,email_token):
    try:
        user=Profiles.objects.get(email_token=email_token)
        user.is_email_verified=True
        user.save()
        return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html')
    except Exception as e:
        return HttpResponse('Invalid Email token')



def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user_obj = User.objects.filter(username=email)
        if not user_obj.exists():
            context = {'message': 'Account not found.', 'class': 'danger'}
            return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html',  context)

        if not user_obj[0].profile.is_email_verified:
            context = {'message': 'Your account is not verified.', 'class': 'danger'}
            return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html',   context)

        user_obj =authenticate(username=email,password=password)
        if user_obj:
            login(request,user_obj)
            return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/header2.html')
        context = {'message': 'Invalid credentials. ', 'class': 'danger'}
        return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html',  context)

    return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html')


def signOut(request):
  logout(request)
  return redirect('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/login.html')




def quick_view(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/quick_view_product.html')
  return HttpResponse(template.render())
def shop(request):

    category=Categories.objects.all()
    colors=Colors.objects.all()
    product = Products.objects.filter(status='PUBLISH')
    Category_id=request.GET.get('category')

    if Category_id:
        product=Products.objects.filter(category=Category_id)
    else:
        product=Products.objects.filter(status='PUBLISH')


    context={'category':category,'colors':colors,'product':product}

    return render(request, 'cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/shop.html', context)

def get_filters(request):
    minMaxPrice=productAttribute.objects.aggregate(Min('price'),Max('price'))
    data={
        'minMaxPrice':minMaxPrice,
    }
    return data



def wishlist(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/wishlist.html')
  return HttpResponse(template.render())

def custom(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/custom.html')
  return HttpResponse(template.render())


def contact(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/contact.html')
  return HttpResponse(template.render())
def faq(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/faq.html')
  return HttpResponse(template.render())

def product(request):
  template = loader.get_template('cloth_websiteProject/flatsome3.uxthemes.com/demos/shop-demos/simple-slider/products.html')
  return HttpResponse(template.render())