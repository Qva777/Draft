from django.urls import path
from E_Shop_API.E_Shop_Cart import views

urlpatterns = [
    #
    path('cart_detail/', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_from_cart'),

    path('empty_cart/', views.empty_cart, name='empty_cart'),

    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    # zim
    # path('cart/pay/', views.pay_cart, name='pay_cart'),
    path('cart/payment/', views.payment_cart, name='payment_cart'),
    path('success_cart/', views.payment_success, name='payment_success'),
]

# from django.urls import path, include
#
# from .views import CartView, CartProductListView
# # from E_Shop_API.E_Shop_Products.views import CancelView, ErrorView
# from E_Shop_API.E_Shop_Cart.views import ProductAddView, payment_cart
#
# urlpatterns = [
#     # Cart post/get/delete
#     path('cart/', CartView.as_view(), name='cart'),
#
#     # Create CartProduct
#     path('product/add/', ProductAddView.as_view(), name='cart'),
#
#     # Auto Create Cart and add item to cart
#     path('product/<int:product_id>/add/', ProductAddView.as_view(), name='add-to-cart'),
#     # Payment
#     path('product/my-cart/pay/', payment_cart, name='payment_cart'),
#     # path('success/', success_cart, name='success'),
#     # path('cancel/', CancelView.as_view(), name='cancel'),
#     # path('error/', ErrorView.as_view(), name='error'),
#     path('cart-products/', CartProductListView.as_view(), name='cart-product-list'),
# ]
#
#
