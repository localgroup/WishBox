from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        
        #Get request
        self.request = request
        # Get the current session key if it exists!
        cart = self.session.get('session_key')
        
        # If the user is new. Create a new session key.
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
            
        self.cart = cart # Makes sure the cart is available on every pages!
        
        
    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        # Cart for logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert to JSON
            _cart = str(self.cart)
            _cart = _cart.replace("\'", "\"")
            #Save _cart to the Profile model
            current_user.update(old_cart=str(_cart))
            
        
    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)
        
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)
            
        self.session.modified = True
        
        # Cart for logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert to JSON
            _cart = str(self.cart)
            _cart = _cart.replace("\'", "\"")
            #Save _cart to the Profile model
            current_user.update(old_cart=str(_cart))
            
        
    def cart_total(self):
        #Get product ids
        product_ids = self.cart.keys()
        
        #Get product from database
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        
        total = 0
        
        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total = total + (product.sale_price * value)
                    else:
                        total = total + (product.price * value)
                    
        return total
    
        
    def __len__(self):
        return len(self.cart)
    
    
    def get_prods(self):
        # Get product ids from cart
        product_ids = self.cart.keys()
        # Search the database
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    
    def get_quants(self):
        quantities = self.cart
        return quantities
    
    
    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        
        #Get the cart
        our_cart = self.cart
        #Update cart
        our_cart[product_id] = product_qty
        
        self.session.modified = True
    
        # Cart for logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert to JSON
            _cart = str(self.cart)
            _cart = _cart.replace("\'", "\"")
            #Save _cart to the Profile model
            current_user.update(old_cart=str(_cart))
        
        my_cart = self.cart
        return my_cart #thing
        
        
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        # Cart for logged in user
        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            #Convert to JSON
            _cart = str(self.cart)
            _cart = _cart.replace("\'", "\"")
            #Save _cart to the Profile model
            current_user.update(old_cart=str(_cart))