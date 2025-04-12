from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem, Order
from decimal import Decimal

def home(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products': products})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('home')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.cartitems.all()
    total = cart.total_price()
    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })

@login_required
def checkout_view(request):
    cart = Cart.objects.get(user=request.user)
    if not cart.cartitems.exists():
        return redirect('cart')

    total = cart.total_price()

    order = Order.objects.create(
        user=request.user,
        cart=cart,
        total_price=Decimal(total),
        is_paid=False
    )

    Cart.objects.create(user=request.user)

    return render(request, 'store/checkout.html', {
        'order': order
    })
