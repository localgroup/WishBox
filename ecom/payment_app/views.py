from django.shortcuts import render

# Create your views here.

def payment_success(request):
    return render(request, "payment_app/payment_success.html", {})