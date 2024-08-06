from django.urls import path
from . import views

urlpatterns = [
    path('payment_success/', views.payment_success, name='payment_success'),
    path('checkout/', views.checkout, name='checkout'),
    path('billing_info/', views.billing_info, name='billing_info'),
    path('process_order/', views.process_order, name='process_order'),
    path('order_shipped/', views.order_shipped, name='order_shipped'),
    path('order_not_shipped/', views.order_not_shipped, name='order_not_shipped'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('orders/<int:pk>/', views.orders, name='orders'),
]
