from django.shortcuts import render, get_object_or_404, HttpResponse
from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.

def cart_summary(request):
    # Get cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products':cart_products, 'quantities':quantities, 'totals':totals})
    
    
def cart_add(request):
    # Get the cart
    cart =  Cart(request)
    
    # GET PRODUCT AND LOOK UP IN DB IF 'POST'
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # Search the DB
        product = get_object_or_404(Product, id=product_id)
        # Save to session
        cart.add(product=product, quantity=product_qty)
        
        # GET CART QUANTITY
        cart_quantity = cart.__len__()
        
        # response = JsonResponse({'Product name': product.name})
        
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, 'Product added to Cart.')
        return response
    
    else:
        return HttpResponse('Invalid request')
    
    
def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
         
        cart.delete(product=product_id)
        
        response = JsonResponse({'product': product_id})
        messages.success(request, 'Item deleted from cart.')
        return response
    
    
def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        
        cart.update(product=product_id, quantity=product_qty)
        
        response = JsonResponse({'qty': product_qty})
        messages.success(request, 'Product Updated.')
        return response
    
    
    
