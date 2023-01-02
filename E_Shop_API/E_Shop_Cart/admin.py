from django.contrib import admin
from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ Register Cart model in admin panel """
    list_display = ('user', 'created_at')
    list_display_links = ('user', 'created_at')
    save_on_top = True


@admin.register(CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    """ Register CartProduct model in admin panel """
    list_display = ('cart', 'product', 'quantity', 'price', 'total_price')
    list_display_links = ('cart', 'product')
    save_on_top = True
