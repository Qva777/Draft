import random
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect
import stripe
from django.contrib import messages

from django.conf import settings
from django.views.generic import TemplateView

from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct
from E_Shop_API.E_Shop_Products.models import Product
from django.views import View
from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator

stripe.api_key = settings.STRIPE_SECRET_KEY

# work
def search(request):
    query = request.GET.get('q')
    product_list = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if not request.user.is_staff:
        product_list = product_list.filter(count__gt=0)
    paginator = Paginator(product_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/search_results.html', {'query': query, 'page_obj': page_obj, 'product_list': product_list})

#  work
# class ProductHomeListView(View):
#     """ Main page/Product list """
#
#
#     # ТУТ НУЖНО ПОЛУЧИТЬ КЛЮЧЬ СЕССИИ
#
#
#     def get(self, request, *args, **kwargs):
#         queryset = Product.objects.all().order_by('-created_at')
#
#         if not request.user.is_staff:
#             queryset = queryset.filter(count__gt=0)
#
#         paginator = Paginator(queryset, 12)
#         page_number = request.GET.get('page')
#         products = paginator.get_page(page_number)
#         return render(request, 'pages/home.html', {'products': products})
#  work
# class ProductHomeListView(View):
#     """Main page/Product list"""
#
#     def get(self, request, *args, **kwargs):
#         queryset = Product.objects.all().order_by('-created_at')
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


class ProductHomeListView(View):
    """Main page/Product list"""

    def get(self, request, *args, **kwargs):
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



class CancelProduct(TemplateView):
    template_name = 'pages/not_found.html'

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№ ВОООООРК start №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

@csrf_exempt
def payment_pro(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    random_products = random.sample(list(Product.objects.all()), 4)  # new  random
    # cart = Cart.objects.get(user=request.user)

    # if request.user.is_authenticated:
    #     # cart = Cart.objects.get(user=request.user)
    #     cart, _ = Cart.objects.get_or_create(user=request.user)
    #     # cart = Cart.objects.get_or_create(user=request.user)
    # else:
    #     session_key = request.session.session_key
    #     if not session_key:
    #         request.session.cycle_key()
    #     # cart = Cart.objects.create(session_key=session_key)
    #     cart, _ = Cart.objects.get_or_create(session_key=session_key)
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


    in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
    cart_product_count = CartProduct.objects.filter(cart=cart).count()

    # if request.user.is_authenticated:
    #     cart = Cart.objects.get(user=request.user)
    #     in_cart = CartProduct.objects.filter(cart=cart, product=product).exists()
    #     cart_product_count = CartProduct.objects.filter(cart=cart).count()

    if cart_product_count >= 10:
        messages.error(request, 'You have reached the maximum limit of 10 products in your cart.')
        # return redirect('cart_detail')








    # work
    if not request.user.is_staff:
        random_products = Product.objects.filter(count__gt=0)
        random_products = random.sample(list(random_products), 4)  # new random
    else:
        random_products = random.sample(list(Product.objects.all()), 4)  # new random


    if product.count < 1:
        error_url = reverse('404')  # , kwargs={'description': 'Product count is less than 1'})
        return redirect(error_url)



    if request.method == "POST":
        # Use Stripe to charge the user's card
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

        # Update the product quantity
        product.count -= 1
        product.save()

        # Return the updated product quantity in the response
        return JsonResponse({"quantity": product.count})


    context = {
        "product": product,
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY,

        "random_products": random_products,
        "in_cart": in_cart,

        "cart_product_count": cart_product_count,
    }

    return render(request, "pages/product_detail.html", context)

# №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№ ВОООООРК end №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№







# test card
# Visa: 4242 4242 4242 4242
# Mastercard: 5105 1051 0510 5100
# American Express: 3782 822463 10005
# Discover: 6011 1111 1111 1117
