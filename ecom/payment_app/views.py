from django.shortcuts import render, redirect
from cart.cart import Cart
from payment_app.models import ShippingAddress
from payment_app.forms import ShippingForm
from django.contrib import messages



def billing_info(request):
    if request.POST:
        # Get cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        shipping_form = ShippingForm(request.POST)
        return render(request, "payment_app/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})

    else:
        messages.success(request, "Access denied!")
        return redirect('home')

def checkout(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    
    if request.user.is_authenticated:
		# Checkout as logged in user
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, "payment_app/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form })
    else:
		# Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment_app/checkout.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_form":shipping_form})


def payment_success(request):
    return render(request, "payment_app/payment_success.html", {})


