from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import HttpResponseForbidden

from .forms import CustomUserCreationForm, ProductForm
from .models import Product, Cart, CartItem, Order

def home(request):
    query = request.GET.get('q', '')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)

    paginator = Paginator(products, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/home.html', {
        'page_obj': page_obj,
        'query': query,
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'store/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
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
    cart, _ = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    items = cart.cartitems.all()
    total = cart.total_price()
    return render(request, 'store/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total
    })

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    return redirect('cart_detail')

@login_required
def checkout_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user, is_ordered=False)
    if not cart.cartitems.exists():
        return redirect('cart_detail')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        card_number = request.POST.get('card_number')

        if payment_method == 'card' and (not card_number or len(card_number.strip()) < 12):
            return render(request, 'store/checkout.html', {
                'cart': cart,
                'error': 'Iltimos, to‘liq karta raqamini kiriting.'
            })

        total = cart.total_price()
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            total_price=total,
            created_at=timezone.now(),
            is_paid=True
        )

        cart.is_ordered = True
        cart.save()
        Cart.objects.create(user=request.user)

        return render(request, 'store/checkout_success.html', {
            'order': order,
            'payment_method': payment_method,
            'card_number': card_number if payment_method == 'card' else None
        })

    return render(request, 'store/checkout.html', {'cart': cart})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})

def is_admin(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(is_admin, login_url='/')
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProductForm()

    return render(request, 'store/add_product.html', {'form': form})

