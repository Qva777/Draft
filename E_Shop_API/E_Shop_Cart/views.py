# Create cart +
# Patch cart +
# delete cart +
# detail cart +
from audioop import reverse

from E_Shop_API.E_Shop_Users.models import Clients
from E_Shop_Frontend.Cart.views import PaymentCartView
from E_Shop_config.settings import BASE_DIR
# payment cart -

from rest_framework import status
from rest_framework import generics
from rest_framework import serializers
from rest_framework.response import Response

from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct, Product
from E_Shop_API.E_Shop_Cart.serializers import CartProductSerializer

import stripe
from django.http import JsonResponse
import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response
# from E_Shop_config.tasks import schedule_cart_deletion
stripe.api_key = settings.STRIPE_SECRET_KEY


class CartProductListAPIView(generics.ListAPIView):
    """ List of Products in Cart """
    serializer_class = CartProductSerializer

    def get_queryset(self):
        user = self.request.user
        session_key = self.request.session.session_key

        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)

            #  celery
            cart.schedule_deletion()  # is it correct ?

        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

            #  celery
            cart.schedule_deletion()  # is it correct ?


        return cart.cart.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        cart_total_price = self.calculate_cart_total_price(queryset)

        response_data = serializer.data
        response_data.append({"total_cart_price": cart_total_price})

        return Response(response_data, status=status.HTTP_200_OK)

    @staticmethod
    def calculate_cart_total_price(cart_products):
        total_price = sum(cart_product.subtotal() for cart_product in cart_products)
        return total_price


class CartProductAPIView(generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView):
    """ API view for adding, updating, and deleting products in the cart """
    serializer_class = CartProductSerializer

    def get_object(self):
        cart_product_id = self.kwargs['cart_product_id']

        try:
            product = Product.objects.get(id=cart_product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product not found')

        user = self.request.user
        session_key = self.request.session.session_key

        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        try:
            cart_product = CartProduct.objects.get(cart=cart, product=product)
        except CartProduct.DoesNotExist:
            raise serializers.ValidationError('Product not found in cart')

        return cart_product

    def post(self, request, *args, **kwargs):
        cart_product = self.get_object()

        quantity = request.data.get('quantity', 1)

        if not isinstance(quantity, int) or quantity < 1:
            return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

        if cart_product.product.count < quantity:
            return Response({'error': 'Quantity exceeds available count'}, status=status.HTTP_400_BAD_REQUEST)

        return self.update_cart_product_quantity(cart_product, quantity)

    def patch(self, request, *args, **kwargs):
        cart_product = self.get_object()

        quantity = request.data.get('quantity')

        if quantity is not None:
            if not isinstance(quantity, int) or quantity < 1:
                return Response({'error': 'Invalid quantity'}, status=status.HTTP_400_BAD_REQUEST)

            if cart_product.product.count < quantity:
                return Response({'error': 'Quantity exceeds available count'}, status=status.HTTP_400_BAD_REQUEST)

            return self.update_cart_product_quantity(cart_product, quantity)

        return Response({'message': 'No changes detected'}, status=status.HTTP_200_OK)

    def update_cart_product_quantity(self, cart_product, quantity):
        cart_product.quantity = quantity
        cart_product.save()

        serializer = self.get_serializer(cart_product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        cart_product = self.get_object()
        cart_product.delete()

        return Response({'message': 'Product removed from cart'}, status=status.HTTP_200_OK)


stripe.api_key = settings.STRIPE_SECRET_KEY

# class PaymentCartAPIView(APIView):
#     """Processing the cart payment"""
#
#     def get_cart(self, request):
#         user = request.user
#         session_key = request.session.session_key
#
#         if user.is_authenticated:
#             cart, _ = Cart.objects.get_or_create(user=user)
#         else:
#             cart, _ = Cart.objects.get_or_create(session_key=session_key)
#
#         return cart
#
#     def post(self, request):
#         cart = self.get_cart(request)
#         cart_products = CartProduct.objects.filter(cart=cart)
#         line_items = []
#         for cart_product in cart_products:
#             product = cart_product.product
#             if product.count < cart_product.quantity:
#                 return Response({'error': 'The quantity of the product is more than the available amount'})
#
#             line_item = {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': product.name,
#                         'description': product.description,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': cart_product.quantity,
#             }
#             line_items.append(line_item)
#
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=request.build_absolute_uri(reverse('payment_success')),
#             cancel_url=request.build_absolute_uri(reverse('404')),
#             metadata={
#                 'cart_id': str(cart.id)
#             }
#         )
#
#         request.session['checkout_session_id'] = checkout_session.id
#         request.session['cart_id'] = str(cart.id)
#         request.session.modified = True
#
#         return Response({'url': checkout_session.url})

from django.urls import reverse_lazy


class PaymentCartMixin:

    @staticmethod
    def create_line_item(cart_product):
        product = cart_product.product
        if product.count < cart_product.quantity:
            return {'error': 'The quantity of the product is more than the available amount'}

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
        return line_item


class PaymentCartAPIView(APIView, PaymentCartMixin):
    """Processing the cart payment"""

    @staticmethod
    def get_cart(request):
        user = request.user
        session_key = request.session.session_key

        if user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=user)
        else:
            cart, _ = Cart.objects.get_or_create(session_key=session_key)

        return cart

    def post(self, request):
        cart = self.get_cart(request)
        cart_products = CartProduct.objects.filter(cart=cart)
        line_items = [self.create_line_item(cart_product) for cart_product in cart_products]
        error_item = next((item for item in line_items if 'error' in item), None)
        if error_item:
            return Response(error_item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=request.build_absolute_uri(reverse_lazy('payment_success')),
            cancel_url=request.build_absolute_uri(reverse_lazy('404')),
            metadata={
                'cart_id': str(cart.id)
            }
        )

        request.session['checkout_session_id'] = checkout_session.id
        request.session['cart_id'] = str(cart.id)
        request.session.modified = True

        return Response({'url': checkout_session.url})

# class PaymentCartMixin:
#     def create_line_item(self, cart_product):
#         product = cart_product.product
#         if product.count < cart_product.quantity:
#             return {'error': 'The quantity of the product is more than the available amount'}
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
#         return line_item
#
# from django.urls import reverse_lazy
# class PaymentCartAPIView(APIView, PaymentCartMixin):
#     """Processing the cart payment"""
#
#     def get_cart(self, request):
#         user = request.user
#         session_key = request.session.session_key
#
#         if user.is_authenticated:
#             cart, _ = Cart.objects.get_or_create(user=user)
#         else:
#             cart, _ = Cart.objects.get_or_create(session_key=session_key)
#
#         return cart
#
#     def post(self, request):
#         cart = self.get_cart(request)
#         cart_products = CartProduct.objects.filter(cart=cart)
#         line_items = [self.create_line_item(cart_product) for cart_product in cart_products]
#         error_item = next((item for item in line_items if 'error' in item), None)
#         if error_item:
#             return Response(error_item)
#
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url=request.build_absolute_uri(reverse_lazy('payment_success')),
#             cancel_url=request.build_absolute_uri(reverse_lazy('404')),
#             metadata={
#                 'cart_id': str(cart.id)
#             }
#         )
#
#         request.session['checkout_session_id'] = checkout_session.id
#         request.session['cart_id'] = str(cart.id)
#         request.session.modified = True
#
#         return Response({'url': checkout_session.url})




# celery
# from django.http import HttpResponse
# from E_Shop_config.tasks import test_func
# def test(request):
#     test_func.delay()
#     return HttpResponse("Done")


