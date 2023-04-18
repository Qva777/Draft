from django.shortcuts import get_object_or_404, redirect, render
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.db.models import Q

import random
import stripe

from django.views import View
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from E_Shop_API.E_Shop_Products.models import Product
from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct

# STRIPE KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


class CancelProduct(TemplateView):
    """Render error page"""
    template_name = 'pages/not_found.html'


class BaseProductView(View):
    """Base view for product-related views"""

    def get_cart(self, request):
        if request.user.is_authenticated:
            cart_queryset = Cart.objects.filter(user=request.user)
            if cart_queryset.exists():
                cart = cart_queryset.first()
            else:
                cart = Cart.objects.create(user=request.user)
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            cart_queryset = Cart.objects.filter(session_key=session_key)
            if cart_queryset.exists():
                cart = cart_queryset.first()
            else:
                cart = Cart.objects.create(session_key=session_key)
        return cart

    def get_random_products(self):
        if not self.request.user.is_staff:
            random_products = Product.objects.filter(count__gt=0)
            random_products = random.sample(list(random_products), 4)
        else:
            random_products = random.sample(list(Product.objects.all()), 4)
        return random_products


class SearchView(BaseProductView):
    """Search field/Search_results"""

    @staticmethod
    def get(request):
        query = request.GET.get('q')
        product_list = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

        if not request.user.is_staff:
            product_list = product_list.filter(count__gt=0)

        paginator = Paginator(product_list, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'query': query,
            'page_obj': page_obj,
            'product_list': product_list,
        }

        return render(request, 'pages/search_results.html', context)


class ProductHomeListView(BaseProductView):
    """Main page/Product list"""

    @staticmethod
    def get(request, *args, **kwargs):
        queryset = Product.objects.filter(active=True).order_by('-created_at')

        if not request.user.is_staff:
            queryset = queryset.filter(count__gt=0)

        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()

        paginator = Paginator(queryset, 12)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        return render(request, 'pages/home.html', {'products': products})


class PaymentView(BaseProductView):
    """Detail views of product"""

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_random_products(self):
        opened_product_id = self.kwargs.get("product_id")
        random_products = Product.objects.filter(active=True).exclude(id=opened_product_id).order_by('?')[:4]
        return random_products

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)
        in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
        cart_product_count = CartProduct.objects.filter(cart=cart).count()

        if cart_product_count >= 10:
            messages.error(request, 'You have reached the maximum limit of 10 products in your cart.')

        random_products = self.get_random_products()

        if product.count < 1:
            error_url = reverse('404')
            return redirect(error_url)

        context = {
            "product": product,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
            "random_products": random_products,
            "in_cart": in_cart,
            "cart_product_count": cart_product_count,
        }

        return render(request, "pages/product_detail.html", context)

    @staticmethod
    def post(request, product_id):
        product = get_object_or_404(Product, id=product_id)
        token = request.POST.get("stripeToken")
        amount = int(product.price * 100)
        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description=product.name,
            )
        except stripe.error.CardError as e:
            return JsonResponse({"error": e.user_message}, status=400)

        product.count -= 1
        product.save()

        # return JsonResponse({"quantity": product.count})
        return render(request, "pages/payment_success.html")

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№ ВОООООРК end №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№


# class PaymentView(View):
#     """View for product payment"""
#
#     def get_stripe_public_key(self):
#         """Helper method to get the Stripe public key"""
#         return settings.STRIPE_PUBLIC_KEY
#
#     def get(self, request, product_id):
#         # Handle GET requests to display the payment page (optional)
#         product = get_object_or_404(Product, id=product_id)
#         context = {
#             "product": product,
#             "stripe_public_key": self.get_stripe_public_key(),
#         }
#         return render(request, "pages/product_detail.html", context)
#
#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         token = request.POST.get("stripeToken")
#         amount = int(product.price * 100)
#
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#
#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency="usd",
#                 source=token,
#                 description=product.name,
#             )
#         except stripe.error.CardError as e:
#             return JsonResponse({"error": e.user_message}, status=400)
#
#         product.count -= 1
#         product.save()
#
#         return JsonResponse({"quantity": product.count})

# class PaymentView(View):
#     """View for product payment"""
#
#     @csrf_exempt
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def post(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         token = request.POST.get("stripeToken")
#         amount = int(product.price * 100)
#
#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency="usd",
#                 source=token,
#                 description=product.name,
#             )
#         except stripe.error.CardError as e:
#             return JsonResponse({"error": e.user_message}, status=400)
#
#         product.count -= 1
#         product.save()
#
#         return JsonResponse({"quantity": product.count})

# class SearchView(View):
#     """ Search field/Search_results """
#
#     @staticmethod
#     def get(request):
#         query = request.GET.get('q')
#         product_list = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
#
#         if not request.user.is_staff:
#             product_list = product_list.filter(count__gt=0)
#
#         paginator = Paginator(product_list, 12)
#         page_number = request.GET.get('page')
#         page_obj = paginator.get_page(page_number)
#
#         context = {
#             'query': query,
#             'page_obj': page_obj,
#             'product_list': product_list,
#         }
#
#         return render(request, 'pages/search_results.html', context)
#
#
# class ProductHomeListView(View):
#     """Main page/Product list"""
#
#     @staticmethod
#     def get(request, *args, **kwargs):
#         queryset = Product.objects.filter(active=True).order_by('-created_at')
#         # queryset = Product.objects.filter(active=True).order_by('?')  # generate Products by random
#
#         if not request.user.is_staff:
#             queryset = queryset.filter(count__gt=0)
#
#         session_key = request.session.session_key
#         if not session_key:
#             request.session.cycle_key()
#
#         paginator = Paginator(queryset, 12)
#         page_number = request.GET.get('page')
#         products = paginator.get_page(page_number)
#         return render(request, 'pages/home.html', {'products': products})
#
#
# class CancelProduct(TemplateView):
#     """ Render error page """
#     template_name = 'pages/not_found.html'
#
#
#
# class PaymentView(View):
#     """ Detail views of product """
#
#     @csrf_exempt
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     @staticmethod
#     def get(request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#
#         if request.user.is_authenticated:
#             cart_queryset = Cart.objects.filter(user=request.user)
#             if cart_queryset.exists():
#                 cart = cart_queryset.first()
#             else:
#                 cart = Cart.objects.create(user=request.user)
#         else:
#             session_key = request.session.session_key
#             if not session_key:
#                 request.session.cycle_key()
#             cart_queryset = Cart.objects.filter(session_key=session_key)
#             if cart_queryset.exists():
#                 cart = cart_queryset.first()
#             else:
#                 cart = Cart.objects.create(session_key=session_key)
#
#         in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
#         cart_product_count = CartProduct.objects.filter(cart=cart).count()
#
#         if cart_product_count >= 10:
#             messages.error(request, 'You have reached the maximum limit of 10 products in your cart.')
#
#         if not request.user.is_staff:
#             random_products = Product.objects.filter(count__gt=0)
#             random_products = random.sample(list(random_products), 4)
#         else:
#             random_products = random.sample(list(Product.objects.all()), 4)
#
#         if product.count < 1:
#             error_url = reverse('404')
#             return redirect(error_url)
#
#         context = {
#             "product": product,
#             "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
#             "random_products": random_products,
#             "in_cart": in_cart,
#             "cart_product_count": cart_product_count,
#         }
#
#         return render(request, "pages/product_detail.html", context)
#
#     @staticmethod
#     def post(request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         token = request.POST.get("stripeToken")
#         amount = int(product.price * 100)
#
#         try:
#             charge = stripe.Charge.create(
#                 amount=amount,
#                 currency="usd",
#                 source=token,
#                 description=product.name,
#             )
#         except stripe.error.CardError as e:
#             return JsonResponse({"error": e.user_message}, status=400)
#
#         product.count -= 1
#         product.save()
#
#         return JsonResponse({"quantity": product.count})

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№ ВОООООРК end №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№


# test card
# Visa: 4242 4242 4242 4242
# Mastercard: 5105 1051 0510 5100
# American Express: 3782 822463 10005
# Discover: 6011 1111 1111 1117
