from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct
from django.contrib import admin


class ProductInline(admin.StackedInline):
    """ отображение cart product в cart """
    model = CartProduct
    extra = 1


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """ cart """
    save_on_top = True

    inlines = [ProductInline]
    list_display = ("user", "total_price", "created_at")
    list_display_links = ("user", "total_price", "created_at")

    def total_price(self, obj):
        """Return the total price of all products in the cart"""
        return '{:.1f}'.format(obj.total_price)

    total_price.admin_order_field = 'total_price'
