# from django.db import models
# from django.contrib.auth.models import User
#
#
# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     image = models.ImageField(upload_to='products/')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.name
#
# class Cart(models.Model):
#     objects = None
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     is_ordered = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username} - Cart"
#
#     def total_price(self):
#         pass
#
#
# class CartItem(models.Model):
#     objects = None
#     cart = models.ForeignKey(Cart, related_name="cartitems", on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#
#     def total_price(self):
#         return self.product.price * self.quantity
#
#     def __str__(self):
#         return f"{self.quantity} of {self.product.name}"
#
#
# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)
#     is_paid = models.BooleanField(default=False)
#
#     def __str__(self):
#         return f"Order {self.id} by {self.user.username}"


from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Cart"

    def total_price(self):
        total = sum(item.total_price() for item in self.cartitems.all())
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cartitems", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

