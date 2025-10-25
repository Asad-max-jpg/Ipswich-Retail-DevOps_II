from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('login/', views.login_view, name='login'),
    path('create-account/', views.create_account, name='create_account'),
    path('contact/', views.contact, name='contact'),
    path('shop/', include('products.urls', namespace='products')),
    path('our-story/', views.our_story, name='our_story'),
    path('admin/', admin.site.urls),
]
