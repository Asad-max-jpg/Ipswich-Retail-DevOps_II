from django.shortcuts import render, redirect
from .models import Order
from .models import Order
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET", "POST"])
def order_create(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == "POST":
        email = request.POST.get('email')
        # The order object isn't used, so prefix with underscore to indicate it's intentional
        _ = Order.objects.create(
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
