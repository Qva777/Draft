from E_Shop_API.E_Shop_Cart.models import Product


def create_product():
    return Product.objects.create(
        name='Test Product',
        description='Test Product Description',
        price=10.0,
        count=5
    )
