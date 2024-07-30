from django.shortcuts import render, redirect
from .models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

from payment_app.forms import ShippingForm
from payment_app.models import ShippingAddress

from django import forms
from django.db.models import Q
import json
from cart.cart import Cart



def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html', {})


def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        # Query the DB
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(category__name__icontains=searched) | Q(description__icontains=searched))
        # IF NULL
        if not searched:
            messages.success(request, "Oops! We could not find that...")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched':searched})
        
    else:
        return render(request, 'search.html', {})


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        
        if user_form.is_valid():
            user_form.save()
            
            login(request, current_user)
            messages.success(request, "Your profile has been succesfully updated")
            return redirect('home')
        return render(request, 'update_user.html', {'user_form':user_form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')
    
    
def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.user)
            
            if form.is_valid():
                form.save()
                messages.success(request, 'Password Changed Succesfully!')
                login(request, current_user)
                return redirect('update_user')
            
            else:
                for error in list(form.errors.value()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form':form})
        
    else:
        messages.success(request, 'You must be logged in!')
        return redirect('login')
    
    
def update_user_info(request):
    if request.user.is_authenticated:
        # Get user
        current_user = Profile.objects.get(user__id=request.user.id)
        # Get user's shipping info
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        
        # User's Billing Form
        info_form = UserInfoForm(request.POST or None, instance=current_user)
        #User's Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        
        if request.method == 'POST':
            if info_form.is_valid():
                info_form.save()
            if shipping_form.is_valid():
                shipping_form.save()
            
            messages.success(request, "Your info has been succesfully updated!")
            return redirect('update_user')
        return render(request, 'update_user_info.html', {'info_form':info_form, 'shipping_form':shipping_form})
    else:
        messages.success(request, "You must be logged in!")
        return redirect('home')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            #Pull the Cart
            current_user = Profile.objects.get(user__id=request.user.id)
            saved_cart = current_user.old_cart
            if saved_cart:
                # Convert to dictionary
                new_cart = json.loads(saved_cart)
                #Get the Cart
                cart = Cart(request)
                #Pull from db
                for key, value in new_cart.items():
                    cart.db_add(product=key, quantity=value)
                
            messages.success(request, ("Welcome back!"))
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('login')        
        
    else:
        return render(request, 'login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')


def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid:
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("Registered sucessfully. Please complete your profile info!"))
            return redirect('update_user_info')
        else:
            messages.success(request, ("Woops! There was a problem. Please try again."))
            return redirect('register')
            
    else:         
        return render(request, 'register.html', {'form':form})
    
    
def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


def category(request, category_type):
    category_type = category_type.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=category_type)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products':products, 'category':category})
        
    except:
        messages.success(request, 'Oops! We couldnot find that...')
        return redirect(request, 'home.html')
    

def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'category_summary.html', {'categories':categories})