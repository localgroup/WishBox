from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    shipping_full_name = models.CharField(max_length=50)
    shipping_email = models.CharField(max_length=50)
    shipping_address1 = models.CharField(max_length=200)
    shipping_address2 = models.CharField(max_length=200, blank=True, null=True)
    shipping_city = models.CharField(max_length=50)
    shipping_state = models.CharField(max_length=50, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=10, blank=True, null=True)
    shipping_country = models.CharField(max_length=50)
    
    #Over-ride Django pluralizer for models!
    class Meta:
        verbose_name_plural = "Shipping Address"
        
    def __str__(self):
        return f"Shipping Address - {str(self.id)}"
    
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    shipping_address = models.TextField(max_length=20000)
    amount_paid = models.DecimalField(max_digits=7, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order - {str(self.id)}"
    
    