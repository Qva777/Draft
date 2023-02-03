import uuid

from django.db import models
from django.db.models import Sum

from E_Shop_API.E_Shop_Products.models import Product
from E_Shop_API.E_Shop_Users.models import Clients
from django.core.exceptions import ValidationError
from django.utils import timezone

# class Cart(models.Model):
#     # id = models.UUIDField(default=uuid.uuid4, primary_key=True)
#     user = models.ForeignKey(Clients, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

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



    # @property
    # def price(self):
    #     new_price = self.product.price * self.quantity
    #     return new_price

# from django.db import models
# from django.db.models.signals import pre_save
#
# from django.http import JsonResponse
# from django.dispatch import receiver
#
# from E_Shop_API.E_Shop_Products.models import Product
# from E_Shop_API.E_Shop_Users.models import Clients
# from django.core.exceptions import ValidationError
#
#
# # ???????????????????????????
# def validate_quantity(quantity, product_count):
#     if quantity > product_count:
#         return JsonResponse({'error': f'The quantity of product is more than the available amount'})
#     elif quantity < 1:
#         return JsonResponse({'error': 'The quantity of product is less than one, impossible'})
#
#
# class Cart(models.Model):
#     """ Cart models/fields  """
#     user = models.OneToOneField(Clients, related_name="users", on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"{self.user.username}"
#
#     @property
#     def total_price(self):
#         return sum(cart_product.total_price for cart_product in self.cartproduct_set.all())
#
#     def decrease_product_quantity(self):
#         for cart_product in self.cartproduct_set.all():
#             product = cart_product.product
#             product.count -= cart_product.quantity
#             product.save()
#
#     """
#     Cart                                                        -
#     total_price                                                 -
#
#     Minimum 3 letters in product name                           -
#     cart/pay/
#     cart/create/                                                +-
#
#
#
#      auto delete after 24 hours                                 -------------------------------------------------------
#      if you pay, auto delete and minus count of product         -------------------------------------------------------
#
#      you can't create a lot of item but cart only one           +
#      """
#
#
# class CartProduct(models.Model):
#     """  CartProduct models/fields  """
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
#     quantity = models.IntegerField()
#     total_price = models.DecimalField(max_digits=5, decimal_places=2, null=True)
#     """
#     если cart  добавлен, то добавить по новой нельзя   +
#     !=  prise <= 0                          +
#         count <= 0                          +
#         count > max(count)                  +
#     ==
#         price * count                       + admin
#         can add a lot of items              +
#         you can update items                +
#
#     Auto Fill in                            +
#         price                               +
#         total_price                         +
#
#     if you press add you should auto create Cart moodel  +
#     """
#
#     def __str__(self):
#         return f"{self.product.name}"
#
#     class Meta:
#         unique_together = ('cart', 'product',)
#
#     def clean(self):
#         """ Quantity validator """
#         if self.quantity < 1:
#             raise ValidationError({'quantity': 'The quantity of product must be greater than 0.'})
#         if self.quantity > self.product.count:
#             raise ValidationError(
#                 {'quantity': f'The quantity of {self.product.count}product is more than the available amount.'})
#
#
# @receiver(pre_save, sender=CartProduct)
# def set_price(sender, instance, **kwargs):
#     """ Before save price * quantity """
#     instance.price = instance.product.price
#     instance.total_price = instance.price * instance.quantity
#
#
#
