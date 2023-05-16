from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.db.models import Q

import base64
import random
import stripe

from django.views import View
from django.views.generic import TemplateView

from email.mime.image import MIMEImage
from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct
from E_Shop_API.E_Shop_Products.models import Product, ProductImage
from E_Shop_Frontend.Cart.views import CartMixin
from django.views.decorators.csrf import csrf_exempt

# STRIPE KEY
stripe.api_key = settings.STRIPE_SECRET_KEY


# class BaseProductView(View):
#     """ Base function for other views """
#
#     @staticmethod
#     def get_cart(request):
#         if request.user.is_authenticated:
#             cart_queryset = Cart.objects.filter(user=request.user)
#             if cart_queryset.exists():
#                 cart = cart_queryset.first()
#             else:
#                 cart = Cart.objects.create(user=request.user)
#                 # celery
#                 cart.schedule_deletion()  # Schedule deletion for anonymous users
#
#         else:
#             session_key = request.session.session_key
#             if not session_key:
#                 request.session.cycle_key()
#             cart_queryset = Cart.objects.filter(session_key=session_key)
#             if cart_queryset.exists():
#                 cart = cart_queryset.first()
#             else:
#                 cart = Cart.objects.create(session_key=session_key)
#                 # celery
#                 cart.schedule_deletion()  # Schedule deletion for anonymous users
#         return cart
#
#     def get_random_products(self):
#         if not self.request.user.is_staff:
#             random_products = Product.objects.filter(count__gt=0)
#             random_products = random.sample(list(random_products), 4)
#         else:
#             random_products = random.sample(list(Product.objects.all()), 4)
#         return random_products


class BaseProductView(View):
    """Base function for other views"""

    def get_cart(self, request):
        """Get the cart based on user authentication or session"""
        if request.user.is_authenticated:
            cart_queryset = Cart.objects.filter(user=request.user)
            if cart_queryset.exists():
                cart = cart_queryset.first()
            else:
                cart = Cart.objects.create(user=request.user)
                cart.schedule_deletion()  # Schedule deletion for anonymous users
        # else:
        #     session_key = request.session.session_key
        #     if not session_key:
        #         request.session.cycle_key()
        #     cart_queryset = Cart.objects.filter(session_key=session_key)
        #     if cart_queryset.exists():
        #         cart = cart_queryset.first()
        #     else:
        #         cart = Cart.objects.create(session_key=session_key)
        #         cart.schedule_deletion()  # Schedule deletion for anonymous users
        # return cart

    def get_random_products(self):
        """Get random products for display"""
        if not self.request.user.is_staff:
            random_products = Product.objects.filter(count__gt=0)
            random_products = random.sample(list(random_products), 4)
        else:
            random_products = random.sample(list(Product.objects.all()), 4)
        return random_products


class SearchView(BaseProductView):
    """ Search field/Search_results """

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
    """ Home page/Product list """

    @staticmethod
    def get(request):
        queryset = Product.objects.filter(active=True).order_by('-created_at')
        # queryset = Product.objects.filter(active=True).order_by('?') generate by random

        if not request.user.is_staff:
            queryset = queryset.filter(count__gt=0)

        session_key = request.session.session_key
        if not session_key:
            request.session.cycle_key()

        paginator = Paginator(queryset, 12)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)
        return render(request, 'pages/home.html', {'products': products})


# def send_inline_photo_email(user_email, email_context):
#     subject = 'Payment Confirmation'
#     html_message = render_to_string('email_templates/payment_confirmation.html', email_context)
#     plain_message = strip_tags(html_message)
#
#     # Create the email message
#     email = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user_email])
#     email.attach_alternative(html_message, 'text/html')
#
#     # Attach the first product image to the email as inline content
#     products = email_context['products']
#     for product in products:
#         image_base64 = product.get('image_base64')
#         if image_base64:
#             email_image = MIMEImage(base64.b64decode(image_base64))
#             email_image.add_header('Content-ID', f'<inline_image_{product["id"]}>')
#             email.attach(email_image)
#             break  # Attach only the first image and then exit the loop
#
#     # Send the email
#     email.send()
class EmailSender:
    @classmethod
    def send_inline_photo_email(cls, user_email, email_context):
        subject = 'Payment Confirmation'
        html_message = render_to_string('email_templates/payment_confirmation.html', email_context)
        plain_message = strip_tags(html_message)

        # Create the email message
        email = EmailMultiAlternatives(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user_email])
        email.attach_alternative(html_message, 'text/html')

        # Attach the first product image to the email as inline content
        products = email_context['products']
        for product in products:
            image_base64 = product.get('image_base64')
            if image_base64:
                email_image = MIMEImage(base64.b64decode(image_base64))
                email_image.add_header('Content-ID', f'<inline_image_{product["id"]}>')
                email.attach(email_image)
                break  # Attach only the first image and then exit the loop

        # Send the email
        email.send()





# class PaymentView(CartMixin, View):
#     """ Detail views of product and Payment """
#
#     @csrf_exempt
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         cart = self.get_cart(request)
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
#         if product.count <= 0:
#             error_message = "Product is out of stock."
#             return redirect(reverse('404') + f'?error_message={error_message}')
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
#         # Reduce the product count only after a successful Stripe charge
#         product.count -= 1
#         product.save()
#         # Get the email from the Stripe charge object
#
#         user_email = charge.source["name"]
#         # Get the product images associated with the product
#
#         product_images = ProductImage.objects.filter(product=product)
#         # Check if there are product images and include only the first image_base64
#
#         image_base64 = None
#         if product_images.exists():
#             first_image = product_images.first()
#             with open(first_image.image.path, "rb") as f:
#                 image_base64 = base64.b64encode(f.read()).decode()
#         # Send the email after a successful payment
#         email_context = {
#             "product": product,
#             "user": request.user,
#             "total_price": product.price,
#             "products": [
#                 {
#                     "id": product.id,
#                     "name": product.name,
#                     "description": product.description,
#                     "count": 1,
#                     "price": product.price,
#                     "image_base64": image_base64,
#                 }
#             ],
#         }
#         # Call the email sending function using the EmailSender class
#         EmailSender.send_inline_photo_email(user_email, email_context)
#         # Return a response indicating the payment was successful
#         return render(request, "pages/payment_success.html")
#         # return JsonResponse({"quantity": product.count})



class CancelProduct(TemplateView):
    """Render error page"""
    template_name = 'pages/not_found.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['error_message'] = self.request.GET.get('error_message', '')
        return context

# мануальное тестирование полюс покрыть тестами фронт и бэкэнд

# протестировать покупку одного(получить емаил)
# купил и письмо пришло но я сомог купить продукт которого нет


# купить корзину получить емаил, почистить код
# купить корзину получить емаил, почистить код (API)
# покрыть тестами

class PaymentProcessor:
    @staticmethod
    def process_payment(product, token, request):
        amount = int(product.price * 100)

        if product.count <= 0:
            error_message = "Product is out of stock."
            return False, error_message

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency="usd",
                source=token,
                description=product.name,
            )
        except stripe.error.CardError as e:
            return False, e.user_message

        # Reduce the product count only after a successful Stripe charge
        product.count -= 1
        product.save()

        # Get the email from the Stripe charge object
        user_email = charge.source["name"]

        # Send the email after a successful payment
        email_context = {
            "product": product,
            "user": request.user,
            "total_price": product.price,
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "count": 1,
                    "price": product.price,
                }
            ],
        }
        EmailSender.send_inline_photo_email(user_email, email_context)

        return True, None


class PaymentView(CartMixin, View):
    """ Detail views of product and Payment """

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)



    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = self.get_cart(request)

        in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
        cart_product_count = CartProduct.objects.filter(cart=cart).count()

        if cart_product_count >= 10:
            messages.error(request, 'You have reached the maximum limit of 10 products in your cart.')

        if not request.user.is_staff:
            random_products = Product.objects.filter(count__gt=0)
            random_products = random.sample(list(random_products), 4)
        else:
            random_products = random.sample(list(Product.objects.all()), 4)

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

        payment_processor = PaymentProcessor()
        success, error_message = payment_processor.process_payment(product, token, request)

        if not success:
            return redirect(reverse('404') + f'?error_message={error_message}')

        return render(request, "pages/payment_success.html")


# class PaymentView(BaseProductView):
#     """ Detail views of product and Payment """
#
#     def get(self, request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         cart = self.get_cart(request)
#         in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
#         cart_product_count = CartProduct.objects.filter(cart=cart).count()
#
#         if cart_product_count >= 10:
#             messages.error(request, 'You have reached the maximum limit of 10 products in your cart.')
#
#         random_products = self.get_random_products()
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
#             # "product_count": product.count,
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
#         # Get the email from the Stripe charge object
#         user_email = charge.source["name"]
#
#         # Get the product images associated with the product
#         product_images = ProductImage.objects.filter(product=product)
#
#         # Check if there are product images and include only the first image_base64
#         image_base64 = None
#         if product_images.exists():
#             first_image = product_images.first()
#             with open(first_image.image.path, "rb") as f:
#                 image_base64 = base64.b64encode(f.read()).decode()
#         #
#         #     # Send the email after a successful payment
#         #     email_context = {
#         #         "product": product,
#         #         "user": request.user,
#         #         "total_price": product.price,
#         #         "products": [
#         #             {
#         #                 "id": product.id,
#         #                 "name": product.name,
#         #                 "description": product.description,
#         #                 "count": 1,
#         #                 "price": product.price,
#         #                 "image_base64": image_base64,
#         #             }
#         #         ],
#         #     }
#         #
#         #     # Call the email sending function
#         #     send_inline_photo_email(user_email, email_context)
#         #
#         #     return render(request, "pages/payment_success.html")
#
#         # Send the email after a successful payment
#         email_context = {
#             "product": product,
#             "user": request.user,
#             "total_price": product.price,
#             "products": [
#                 {
#                     "id": product.id,
#                     "name": product.name,
#                     "description": product.description,
#                     "count": 1,
#                     "price": product.price,
#                     "image_base64": image_base64,
#                 }
#             ],
#         }
#
#         # Call the email sending function using the EmailSender class
#         EmailSender.send_inline_photo_email(user_email, email_context)
#
#         return render(request, "pages/payment_success.html")
# from django.views.decorators.csrf import csrf_exempt
# class PaymentView(View):
#     # """ рабочий вариант, но нет отправки эмейла """
#     """ Detail views of product and Payment """
#
#
#     @csrf_exempt
#     def dispatch(self, request, *args, **kwargs):
#         return super().dispatch(request, *args, **kwargs)
#
#     @staticmethod
#     def get(request, product_id):
#         product = get_object_or_404(Product, id=product_id)
#         cart = None
#
#         if request.user.is_authenticated:
#             cart_queryset = Cart.objects.filter(user=request.user)
#             if cart_queryset.exists():
#                 cart = cart_queryset.first()
#             else:
#                 cart = Cart.objects.create(user=request.user)
#         # else:
#             # session_key = request.session.session_key
#             # if not session_key:
#             #     request.session.cycle_key()
#             # cart_queryset = Cart.objects.filter(session_key=session_key)
#             # if cart_queryset.exists():
#             #     cart = cart_queryset.first()
#             # else:
#             #     cart = Cart.objects.create(session_key=session_key)
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
#         if product.count <= 0:
#             return JsonResponse({"error": "Product is out of stock."}, status=400)
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
#         # Reduce the product count only after a successful Stripe charge
#         product.count -= 1
#         product.save()
#
#         # Get the email from the Stripe charge object
#         user_email = charge.source["name"]
#
#         # Get the product images associated with the product
#         product_images = ProductImage.objects.filter(product=product)
#
#         # Check if there are product images and include only the first image_base64
#         image_base64 = None
#         if product_images.exists():
#             first_image = product_images.first()
#             with open(first_image.image.path, "rb") as f:
#                 image_base64 = base64.b64encode(f.read()).decode()
#
#         # Send the email after a successful payment
#         email_context = {
#             "product": product,
#             "user": request.user,
#             "total_price": product.price,
#             "products": [
#                 {
#                     "id": product.id,
#                     "name": product.name,
#                     "description": product.description,
#                     "count": 1,
#                     "price": product.price,
#                     "image_base64": image_base64,
#                 }
#             ],
#         }
#
#         # Call the email sending function using the EmailSender class
#         EmailSender.send_inline_photo_email(user_email, email_context)
#
#         # Return a response indicating the payment was successful
#         return JsonResponse({"quantity": product.count})
#
#     # @staticmethod
#     # def post(request, product_id):
#     #     product = get_object_or_404(Product, id=product_id)
#     #     token = request.POST.get("stripeToken")
#     #     amount = int(product.price * 100)
#     #
#     #     if product.count <= 0:
#     #         return JsonResponse({"error": "Product is out of stock."}, status=400)
#     #
#     #     try:
#     #         charge = stripe.Charge.create(
#     #             amount=amount,
#     #             currency="usd",
#     #             source=token,
#     #             description=product.name,
#     #         )
#     #     except stripe.error.CardError as e:
#     #         return JsonResponse({"error": e.user_message}, status=400)
#     #
#     #     # # Reduce the product count only after a successful Stripe charge
#     #     # product.count -= 1
#     #     # product.save()
#     #     #
#     #     # return JsonResponse({"quantity": product.count})
#     #     # except stripe.error.CardError as e:
#     #     #     return JsonResponse({"error": e.user_message}, status=400)
#     #
#     #     product.count -= 1
#     #     product.save()
#     #
#     #     # Get the email from the Stripe charge object
#     #     user_email = charge.source["name"]
#     #
#     #     # Get the product images associated with the product
#     #     product_images = ProductImage.objects.filter(product=product)
#     #
#     #     # Check if there are product images and include only the first image_base64
#     #     image_base64 = None
#     #     if product_images.exists():
#     #         first_image = product_images.first()
#     #         with open(first_image.image.path, "rb") as f:
#     #             image_base64 = base64.b64encode(f.read()).decode()
#     #
#     #     # Send the email after a successful payment
#     #     email_context = {
#     #         "product": product,
#     #         "user": request.user,
#     #         "total_price": product.price,
#     #         "products": [
#     #             {
#     #                 "id": product.id,
#     #                 "name": product.name,
#     #                 "description": product.description,
#     #                 "count": 1,
#     #                 "price": product.price,
#     #                 "image_base64": image_base64,
#     #             }
#     #         ],
#     #     }
#     #
#     #     # Call the email sending function using the EmailSender class
#     #     EmailSender.send_inline_photo_email(user_email, email_context)
from django.http import HttpResponseRedirect