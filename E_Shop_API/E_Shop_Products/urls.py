from django.urls import path
from E_Shop_API.E_Shop_Products import views

urlpatterns = [
    # CRUD permissions Is_admin
    path('create-product/', views.ProductCreateView.as_view(), name='create_product'),
    path('product/<int:pk>/', views.ProductView.as_view(), name='product_detail'),

    # Whole Item List
    path('products/', views.ProductListView.as_view(), name='all_product'),



    # preparing to delete
    # payment one product
    # path('product/<int:product_id>/pay/', views.payment_pro, name='payment_pro'),
    #     path('success_pro/', views.success_pro, name='success_pro'),
    #     path('cancel_pro/', views.cancel_pro, name='cancel_pro'),
    # preparing to delete
]
