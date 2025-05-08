from django.urls import path
from . import views
from .views import register_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', register_view, name='register'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    # path('cart/', views.cart_view, name='cart'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('create-product/', views.create_product, name='create_product'),


]
