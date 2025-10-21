from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def cart(request):
    return render(request, 'cart.html')

def checkout(request):
    return render(request, 'checkout.html')

def orders(request):
    return render(request, 'orders.html')

def login_view(request):
    return render(request, 'login.html')

def create_account(request):
    return render(request, 'create_account.html')

def contact(request):
    return render(request, 'contact.html')

def our_story(request):
    return render(request, 'our_story.html')
