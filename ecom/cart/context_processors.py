from .cart import Cart


# Context processor for cart so that it works on all pages.
def cart(request):
    # Return the default data from the cart
    return {'cart': Cart(request)} 