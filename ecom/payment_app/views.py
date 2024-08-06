from django.shortcuts import render, redirect
from cart.cart import Cart
from payment_app.models import ShippingAddress, Order, OrderItem
from payment_app.forms import ShippingForm, PaymentForm
from django.contrib import messages
from django.contrib.auth.models import User
from store.models import Product


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        return render(request, "payment_app/orders.html", {"items":items, "order":order})
    
    else:
        messages.success(request, "Access denied!")
        return redirect('home')


def admin_dashboard(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return render(request, "payment_app/admin_dashboard.html", {})
    
    else:
        messages.success(request, "Access denied!")
        return redirect('home')


def order_shipped(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        return render(request, "payment_app/order_shipped.html", {"orders":orders})
    
    else:
        messages.success(request, "Access denied!")
        return redirect('home')
    
    
def order_not_shipped(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        return render(request, "payment_app/order_not_shipped.html", {"orders":orders})
    
    else:
        messages.success(request, "Access denied!")
        return redirect('home')    
    

def process_order(request):
    if request.POST:
        # Get cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # Get billing info from the last page
        payment_form = PaymentForm(request.POST or None)
        
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        
        #Get Order Info...
        full_name = my_shipping['shipping_full_name']
        phone_number = my_shipping['shipping_phone']
        # Create Shipping Addesss from session info
        shipping_address = (
            f"{my_shipping['shipping_address1']}\n"
            f"{my_shipping['shipping_address2']}\n"
            f"{my_shipping['shipping_city']}, {my_shipping['shipping_state']} {my_shipping['shipping_zipcode']}\n"
            f"{my_shipping['shipping_country']}\n"
        )
        amount_paid = totals
        
        # Create an order
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, phone=phone_number, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add order items...
            # Get the order id
            order_id = create_order.pk
            
            # Get product info
            for product in cart_products():
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #Create order items
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user_id=user.id, quantity=value, price=price)
                        create_order_item.save()
                        
            # Delete or update the cart after placing an order
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            
            messages.success(request, "Order placed!")
            return redirect('home')
            
        else:
            create_order = Order(full_name=full_name, phone=phone_number, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            
            # Add order items...
            # Get the order id
            order_id = create_order.pk
            
            # Get product info
            for product in cart_products():
                product_id = product.id
                
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                    
                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        #Create order items
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=price)
                        create_order_item.save()
                        
            # Delete or update the cart after placing an order
            for key in list(request.session.keys()):
                if key == "session_key":
                    del request.session[key]
            
            
            messages.success(request, "Order placed!")
            return redirect('home')
    
    else:
        messages.success(request, "Access denied!")
        return redirect('home')
    # return render(request, "payment_app/process_order.html", {})


def billing_info(request):
    if request.POST:
        # Get cart
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        
        # Create a session with shipping info
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        
        # User Authentication
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment_app/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
        
        else:
            billing_form = PaymentForm()
            return render(request, "payment_app/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "billing_form":billing_form})
    
        shipping_form = request.POST
        return render(request, "payment_app/billing_info.html", {"cart_products":cart_products, "quantities":quantities, "totals":totals, "shipping_info":request.POST, "shipping_form":shipping_form})

    
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


