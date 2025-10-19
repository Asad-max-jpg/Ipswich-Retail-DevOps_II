from django.shortcuts import render, redirect
from .models import Order, OrderItem
from products.models import Product
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def order_create(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # minimal: in real app validate and process cart
        order = Order.objects.create(email=email)
        # placeholder: assume cart items posted as product_id:qty pairs
        # in PoC we skip cart processing complexity
        return render(request, 'orders/order_success.html', {'order': order})
    return render(request, 'orders/order_form.html')
