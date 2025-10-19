from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include

def home(request):
    return render(request, 'home.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('shop/', include('products.urls', namespace='products')),
    path('orders/', include('orders.urls', namespace='orders')),
]
    