from django.urls import path, include

from .views import CartView
# from E_Shop_API.E_Shop_Products.views import CancelView, ErrorView
from E_Shop_API.E_Shop_Cart.views import ProductAddView, payment_cart

urlpatterns = [
    # Cart post/get/delete
    path('cart/', CartView.as_view(), name='cart'),

    # Create CartProduct
    path('product/add/', ProductAddView.as_view(), name='cart'),

    # Auto Create Cart and add item to cart
    path('product/<int:product_id>/add/', ProductAddView.as_view(), name='add-to-cart'),
    # Payment
    path('product/my-cart/pay/', payment_cart, name='payment_cart'),
    # path('success/', success_cart, name='success'),
    # path('cancel/', CancelView.as_view(), name='cancel'),
    # path('error/', ErrorView.as_view(), name='error'),
]


