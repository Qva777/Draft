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

