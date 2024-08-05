from django.contrib import admin
from . models import ShippingAddress, Order, OrderItem

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


#Create an OrderItem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
    
    
#Extend our Order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    # fields = ["full_name"]
    inlines = [OrderItemInline]
    
    
#Unregister Order model
admin.site.unregister(Order)

# Re-register Order and OrderAdmin
admin.site.register(Order, OrderAdmin)