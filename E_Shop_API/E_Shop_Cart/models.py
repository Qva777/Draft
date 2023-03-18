from django.db import models
from E_Shop_API.E_Shop_Users.models import Clients
from E_Shop_API.E_Shop_Products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(Clients, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_cart_owner(self):
        if self.user:
            return self.user
        else:
            return self.session_key

    @property
    def total_price(self):
        """Calculate the total price of all products in the cart"""
        total = 0
        for item in self.cart.all():
            total += item.product.price * item.quantity
        return total


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")
    quantity = models.IntegerField(default=0)
    # new line
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    class Meta:
        unique_together = ('cart', 'product')

    def subtotal(self):
        return self.product.price * self.quantity