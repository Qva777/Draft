from E_Shop_API.E_Shop_Products.models import Product
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from .models import Cart, CartProduct
import stripe

# def add_to_cart(request, product_id):
#     """Add a product to the cart"""
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     product = get_object_or_404(Product, id=product_id)
#
#     # check if requested quantity is greater than the product count
#     quantity = int(request.POST.get('quantity', 1))
#     if quantity > product.count:
#         quantity = product.count
#
#     # limit the number of products to 10
#     # check if adding this quantity would exceed the limit of 10 products in the cart
#     if CartProduct.objects.filter(cart=cart).count() >= 10:
#         messages.warning(request, "You can only add up to 10 products to your cart.")
#         # return redirect('payment_pro')
#         return redirect(reverse('payment_pro', kwargs={'product_id': product_id}))
#
#     else:
#         cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
#         cart_product.quantity += quantity
#         cart_product.save()
#
#         # messages.success(request, f"{product.name} has been added to your cart.")
#
#         return redirect('cart_detail')

def add_to_cart(request, product_id):
    """Add a product to the cart"""
    if request.user.is_authenticated:
        # User is authenticated
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    product = get_object_or_404(Product, id=product_id)

    # Check if requested quantity is greater than the product count
    quantity = int(request.POST.get('quantity', 1))
    if quantity > product.count:
        quantity = product.count

    # Limit the number of products to 10
    # Check if adding this quantity would exceed the limit of 10 products in the cart
    if CartProduct.objects.filter(cart=cart).count() >= 10:
        messages.warning(request, "You can only add up to 10 products to your cart.")
        return redirect(reverse('payment_pro', kwargs={'product_id': product_id}))

    else:
        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()

        return redirect('cart_detail')



# def update_cart(request, product_id):
#     cart, created = Cart.objects.get_or_create(user=request.user)
#     product = get_object_or_404(Product, id=product_id)
#     cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
#
#     if request.method == 'POST':
#         action = request.POST.get('action')
#
#         if action == 'add':
#             cart_product.quantity += 1
#         elif action == 'remove':
#             cart_product.quantity -= 1
#
#         elif action == 'update':
#             quantity = int(request.POST.get('quantity'))
#             cart_product.quantity = quantity
#
#         cart_product.save()
#
#     return redirect('cart_detail')
def update_cart(request, product_id):
    if request.user.is_authenticated:
        # User is authenticated
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    product = get_object_or_404(Product, id=product_id)
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'add':
            cart_product.quantity += 1
        elif action == 'remove':
            cart_product.quantity -= 1
        elif action == 'update':
            quantity = int(request.POST.get('quantity'))
            cart_product.quantity = quantity

        cart_product.save()

    return redirect('cart_detail')


# def cart_detail(request):
#     """View the contents of the cart"""
#
#     cart = Cart.objects.get(user=request.user)
#     cart_products = CartProduct.objects.filter(cart=cart).order_by('-created_at')
#
#     for cart_product in cart_products:
#         if cart_product.product.count == 0 or cart_product.quantity > cart_product.product.count:
#             cart_product.delete()
#
#     return render(request, 'cart_detail.html', {'cart': cart, 'cart_products': cart_products})


# def cart_detail(request):
#     """View the contents of the cart"""
#
#     cart, created = Cart.objects.get_or_create(user=request.user)
#
#     cart_products = CartProduct.objects.filter(cart=cart).order_by('-created_at')
#
#     for cart_product in cart_products:
#         if cart_product.product.count == 0 or cart_product.quantity > cart_product.product.count:
#             cart_product.delete()
#
#     return render(request, 'cart_detail.html', {'cart': cart, 'cart_products': cart_products})



def cart_detail(request):
    """View the contents of the cart"""

    if request.user.is_authenticated:
        # User is authenticated
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart, created = Cart.objects.get_or_create(session_key=session_key)

    cart_products = CartProduct.objects.filter(cart=cart).order_by('-created_at')

    for cart_product in cart_products:
        if cart_product.product.count == 0 or cart_product.quantity > cart_product.product.count:
            cart_product.delete()

    return render(request, 'cart_detail.html', {'cart': cart, 'cart_products': cart_products})



# def cart_detail(request):
#     """View the contents of the cart"""
#
#     if isinstance(request.user, AnonymousUser):
#         # User is anonymous
#         cart = None
#         cart_products = None
#     else:
#         # User is authenticated
#         cart = Cart.objects.get(user=request.user)
#         cart_products = CartProduct.objects.filter(cart=cart).order_by('-created_at')
#
#         for cart_product in cart_products:
#             if cart_product.product.count == 0 or cart_product.quantity > cart_product.product.count:
#                 cart_product.delete()
#
#     return render(request, 'cart_detail.html', {'cart': cart, 'cart_products': cart_products})



# def remove_cart(request, product_id):
#     """Remove a product from the cart"""
#     cart = Cart.objects.get(user=request.user)
#     product = get_object_or_404(Product, pk=product_id)
#     cart_product = CartProduct.objects.get(cart=cart, product=product)
#     cart_product.delete()
#     return redirect('cart_detail')
#
#
# def empty_cart(request):
#     """Remove all products from the cart"""
#     cart = Cart.objects.get(user=request.user)
#     cart_products = CartProduct.objects.filter(cart=cart)
#     cart_products.delete()
#     return redirect('cart_detail')



stripe.api_key = settings.STRIPE_SECRET_KEY

# def payment_cart(request):
#     cart = Cart.objects.get(user=request.user)
#     cart_products = CartProduct.objects.filter(cart=cart)
#     line_items = []
#     for cart_product in cart_products:
#         product = cart_product.product
#         if product.count < cart_product.quantity:
#             return JsonResponse({'error': 'The quantity of product is more than the available amount'})
#
#         line_item = {
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.name,
#                     'description': product.description,
#                 },
#                 'unit_amount': int(product.price * 100),
#             },
#             'quantity': cart_product.quantity,
#         }
#         line_items.append(line_item)
#
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         success_url=request.build_absolute_uri(reverse('payment_success')),
#         cancel_url=request.build_absolute_uri(reverse('404')),
#         metadata={
#             'cart_id': cart.id
#         }
#     )
#
#     request.session['checkout_session_id'] = checkout_session.id
#
#     return redirect(checkout_session.url)


def payment_success(request):
    # Get the cart object from the metadata of the checkout session
    checkout_session_id = request.session.get('checkout_session_id')
    checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
    cart_id = checkout_session.metadata.get('cart_id')
    cart = Cart.objects.get(id=cart_id)

    # Clear the cart
    # cart.cartproducts.all().delete()
    cart.cart.all().delete()
    return render(request, "payment_success.html")


# def payment_cart(request):
#     user = request.user
#     cart = Cart.objects.get(user=user)
#     line_items = []
#     for cart_product in cart.cartproduct_set.all():
#         product = cart_product.product
#         if product.count < cart_product.quantity:
#             # return redirect(reverse('cart'))
#             return JsonResponse({'error': 'The quantity of product is more than the available amount yyyyyy'})
#
#
#         line_item = {
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.name,
#                     'description': product.description,
#                 },
#                 'unit_amount': int(product.price * 100),
#             },
#             'quantity': cart_product.quantity,
#         }
#         line_items.append(line_item)
#
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         # success_url=request.build_absolute_uri(reverse('success')),
#         success_url='http://127.0.0.1:8000/api/success_cart/',
#
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#         metadata={
#             'cart_id': cart.id
#         }
#     )
#
#     # Store the checkout session ID as a session variable
#     request.session['checkout_session_id'] = checkout_session.id
#
#     return redirect(checkout_session.url)





# NEW LINE  end anonimus
def remove_cart(request, product_id):
    """Remove a product from the cart"""
    if request.user.is_authenticated:
        # User is authenticated
        cart = Cart.objects.get(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.get(session_key=session_key)

    product = get_object_or_404(Product, pk=product_id)
    cart_product = CartProduct.objects.get(cart=cart, product=product)
    cart_product.delete()
    return redirect('cart_detail')


def empty_cart(request):
    """Remove all products from the cart"""
    if request.user.is_authenticated:
        # User is authenticated
        cart = Cart.objects.get(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.get(session_key=session_key)

    cart_products = CartProduct.objects.filter(cart=cart)
    cart_products.delete()
    return redirect('cart_detail')


def payment_cart(request):
    if request.user.is_authenticated:
        # User is authenticated
        cart = Cart.objects.get(user=request.user)
    else:
        # User is anonymous
        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()
        cart = Cart.objects.get(session_key=session_key)

    cart_products = CartProduct.objects.filter(cart=cart)
    line_items = []
    for cart_product in cart_products:
        product = cart_product.product
        if product.count < cart_product.quantity:
            return JsonResponse({'error': 'The quantity of the product is more than the available amount'})

        line_item = {
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': product.name,
                    'description': product.description,
                },
                'unit_amount': int(product.price * 100),
            },
            'quantity': cart_product.quantity,
        }
        line_items.append(line_item)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success')),
        cancel_url=request.build_absolute_uri(reverse('404')),
        metadata={
            'cart_id': cart.id
        }
    )

    request.session['checkout_session_id'] = checkout_session.id

    return redirect(checkout_session.url)


# NEW LINE  end anonimus

















# def update_cart(request, product_id):
#     """Update the quantity of a product in the cart"""
#     cart = Cart.objects.get(user=request.user)
#     product = get_object_or_404(Product, id=product_id)
#     cart_product = CartProduct.objects.get(cart=cart, product=product)
#     action = request.POST.get('action')
#     if action == 'add':
#         cart_product.quantity += 1
#         cart_product.save()
#     elif action == 'remove':
#         cart_product.quantity -= 1
#         if cart_product.quantity < 1:
#             cart_product.delete()
#         else:
#             cart_product.save()
#     return redirect('cart_detail')


# from django import template
#
# register = template.Library()
#
# @register.filter
# def sort_by_quantity(queryset):
#     return sorted(queryset, key=lambda item: item.quantity)
#
# def update_cart(request, product_id):
#     """Update the quantity of a product in the cart"""
#     cart = Cart.objects.get(user=request.user)
#     product = get_object_or_404(Product, id=product_id)
#     cart_product = CartProduct.objects.get(cart=cart, product=product)
#     if request.method == 'POST':
#         quantity = request.POST.get('quantity')
#         if quantity.isdigit() and int(quantity) > 0:
#             old_quantity = cart_product.quantity
#             new_quantity = int(quantity)
#             cart_product.quantity = new_quantity
#             cart_product.save()
#             cart_products = list(cart.cartproduct_set.all())
#             if old_quantity < new_quantity:
#                 for i in range(cart_products.index(cart_product), 0, -1):
#                     if cart_products[i-1].quantity >= new_quantity:
#                         break
#                     cart_products[i], cart_products[i-1] = cart_products[i-1], cart_products[i]
#             else:
#                 for i in range(cart_products.index(cart_product), len(cart_products)-1):
#                     if cart_products[i+1].quantity <= new_quantity:
#                         break
#                     cart_products[i], cart_products[i+1] = cart_products[i+1], cart_products[i]
#             request.session['cart_products'] = [cp.id for cp in cart_products]
#     return redirect('cart_detail')


# import stripe
# from django.urls import reverse
#
# from rest_framework import status
# from rest_framework import permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
#
# from django.http import Http404, JsonResponse
# from django.shortcuts import get_object_or_404
#
# from E_Shop_API.E_Shop_Products.models import Product
# from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct, validate_quantity
# from E_Shop_API.E_Shop_Cart.serializers import CartSerializer, CartProductSerializer, CartProductDetailSerializer
# from django.conf import settings
# from django.shortcuts import redirect
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# def return_serializer(serializer, product):
#     error_response = validate_quantity(
#         serializer.validated_data['quantity'],
#         product.count
#     )
#     if error_response:
#         return error_response
#
#
# class CartView(APIView):
#     """ Cart view """
#     permission_classes = [permissions.IsAuthenticated, ]
#
#     @staticmethod
#     def post(request, *args, **kwargs):
#         """ Create my shopping cart """
#         data = request.data.copy()
#         data['user'] = request.user.id
#         serializer = CartSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @staticmethod
#     def get(request):
#         """ GET whole shopping carts """
#         if not request.user.is_staff:
#             """ Only admin/staff can see """
#             raise Http404
#         queryset = Cart.objects.all()
#         serializer = CartSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def delete(self, request):
#         """ DELETE my shopping cart """
#         cart = get_object_or_404(Cart, user=request.user)
#         if cart.user != self.request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         cart.delete()
#         return Response({"message": "Cart was successfully deleted"})
#
#
# class ProductAddView(APIView):
#     """ Adds CartProduct to Cart """
#     permission_classes = [permissions.IsAuthenticated]
#
#     @staticmethod
#     def post(request, product_id):
#         """ Adds Product into Cart model """
#         user = request.user
#         product = Product.objects.get(id=product_id)
#         serializer = CartProductSerializer(data=request.data)
#
#         if serializer.is_valid():
#             error_response = return_serializer(serializer, product)
#             if error_response:
#                 """ Called when there are errors with the quantity """
#                 return error_response
#             try:
#                 """ If Cart DoesNotExist Auto create and adds there product"""
#                 cart = Cart.objects.get(user=user)
#             except Cart.DoesNotExist:
#                 cart = Cart.objects.create(user=user)
#
#             try:
#                 cart_product = CartProduct.objects.get(cart=cart, product=product)
#                 if cart_product:
#                     return Response({"error": "This item is already in your cart"}, status=status.HTTP_400_BAD_REQUEST)
#                 # cart_product.quantity += serializer.validated_data['quantity']
#                 cart_product.save()
#             except CartProduct.DoesNotExist:
#                 serializer.save(cart=cart, product=product, price=product.price,
#                                 total_price=product.price * serializer.validated_data['quantity'])
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     @staticmethod
#     def get(request, product_id):
#         """ GET Detail about added Product """
#         user = request.user
#         cart = Cart.objects.get(user=user)
#         try:
#             product = Product.objects.get(id=product_id)
#             cart_product = CartProduct.objects.get(cart=cart, product=product)
#             serializer = CartProductDetailSerializer(cart_product)
#             return Response(serializer.data)
#         except (Product.DoesNotExist, CartProduct.DoesNotExist):
#             return Response({"error": "Product or cart product not found"}, status=status.HTTP_404_NOT_FOUND)
#
#     @staticmethod
#     def patch(request, product_id):
#         """ PATCH change CartProduct quantity """
#         user = request.user
#         cart = Cart.objects.get(user=user)
#         try:
#             product = Product.objects.get(id=product_id)
#             cart_product = CartProduct.objects.get(cart=cart, product=product)
#             serializer = CartProductSerializer(cart_product, data=request.data, partial=True)
#
#             if serializer.is_valid():
#                 error_response = return_serializer(serializer, product)
#                 if error_response:
#                     """ Called when there are errors with the quantity """
#                     return error_response
#                 serializer.save()
#                 return Response(serializer.data)
#
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Product.DoesNotExist:
#             return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
#         except CartProduct.DoesNotExist:
#             return Response({"error": "Cart product not found"}, status=status.HTTP_404_NOT_FOUND)
#
#     @staticmethod
#     def delete(request, product_id):
#         """ DELETE CartProduct from my Cart """
#         user = request.user
#         cart = Cart.objects.get(user=user)
#         product = Product.objects.get(id=product_id)
#         cart_product = CartProduct.objects.get(cart=cart, product=product)
#         cart_product.delete()
#         return Response({"message": "Cart product was successfully deleted"})
#
#
# class CartProductListView(APIView):
#     """ Lists all the CartProduct instances in the current user's cart """
#     permission_classes = [permissions.IsAuthenticated]
#
#     def get(self, request):
#         cart = get_object_or_404(Cart, user=request.user)
#         cart_products = CartProduct.objects.filter(cart=cart)
#         serializer = CartProductDetailSerializer(cart_products, many=True)
#         return Response(serializer.data)
#
#
#
# """ work"""
# # def payment(request):
# #     """ checkout """
# #     user = request.user
# #     cart = Cart.objects.get(user=user)
# #     line_items = []
# #     for cart_product in cart.cartproduct_set.all():
# #         line_item = {
# #             'price_data': {
# #                 'currency': 'usd',
# #                 'product_data': {
# #                     'name': cart_product.product.name,
# #                     'description': cart_product.product.description,
# #                 },
# #                 'unit_amount': int(cart_product.price * 100),
# #             },
# #             'quantity': cart_product.quantity,
# #         }
# #         line_items.append(line_item)
# #
# #     checkout_session = stripe.checkout.Session.create(
# #         payment_method_types=['card'],
# #         line_items=line_items,
# #         mode='payment',
# #         success_url=request.build_absolute_uri(reverse('success')),
# #         cancel_url=request.build_absolute_uri(reverse('cancel')),
# #         metadata={
# #             'cart_id': cart.id
# #         }
# #     )
# #
# #     # Store the checkout session ID as a session variable
# #     request.session['checkout_session_id'] = checkout_session.id
# #
# #     return redirect(checkout_session.url)
#
#
#
# def payment_cart(request):
#     user = request.user
#     cart = Cart.objects.get(user=user)
#     line_items = []
#     for cart_product in cart.cartproduct_set.all():
#         product = cart_product.product
#         if product.count < cart_product.quantity:
#             # return redirect(reverse('cart'))
#             return JsonResponse({'error': 'The quantity of product is more than the available amount yyyyyy'})
#
#
#         line_item = {
#             'price_data': {
#                 'currency': 'usd',
#                 'product_data': {
#                     'name': product.name,
#                     'description': product.description,
#                 },
#                 'unit_amount': int(product.price * 100),
#             },
#             'quantity': cart_product.quantity,
#         }
#         line_items.append(line_item)
#
#     checkout_session = stripe.checkout.Session.create(
#         payment_method_types=['card'],
#         line_items=line_items,
#         mode='payment',
#         # success_url=request.build_absolute_uri(reverse('success')),
#         success_url='http://127.0.0.1:8000/api/success_cart/',
#
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#         metadata={
#             'cart_id': cart.id
#         }
#     )
#
#     # Store the checkout session ID as a session variable
#     request.session['checkout_session_id'] = checkout_session.id
#
#     return redirect(checkout_session.url)
#
#
#
# """
# paymant must be
# """
#
# def success_cart(request):
#     # Retrieve the checkout session ID from the session
#     checkout_session_id = request.session.get('checkout_session_id')
#     checkout_session = stripe.checkout.Session.retrieve(checkout_session_id)
#
#     # Subtract the number of products from the product model
#     cart_id = checkout_session['metadata']['cart_id']
#     cart = Cart.objects.get(id=cart_id)
#     for cart_product in cart.cartproduct_set.all():
#         product = cart_product.product
#         product.count -= cart_product.quantity
#         product.save()
#
#     # Delete the Cart
#     cart.delete()
#
#     # Clear the checkout session ID from the session
#     request.session.pop('checkout_session_id', None)
#
#     # Redirect the user to a success page
#     return redirect('success_page')
# """
# paymant
# """
#
#
#
#
