from django.urls import path
from E_Shop_Frontend.Products import views

urlpatterns = [

    # payment one product
    path('product/<int:product_id>/pay/', views.payment_pro, name='payment_pro'),
    # path('success_pro/', views.success, name='success_purchase'),
    path('404/', views.CancelProduct.as_view(), name='cancel_purchase'),

]
