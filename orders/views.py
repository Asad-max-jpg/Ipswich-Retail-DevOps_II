from django.shortcuts import render, redirect
from .models import Order, OrderItem
from products.models import Product
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')
        
    if request.method == "POST":
        email = request.POST.get('email')
        order = Order.objects.create(
            email=email,
            user=request.user
        )
        return redirect('orders:list')
    return render(request, 'orders/order_form.html')

def order_list(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})
