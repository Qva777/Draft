from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions
from E_Shop_API.E_Shop_Products.serializers import ProductSerializer
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator
from django.views.generic import View
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.shortcuts import redirect, render
import stripe
from django.conf import settings
from django.views.generic import TemplateView

from E_Shop_API.E_Shop_Products.models import Product
from django.views import View
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY


# def product_list(request):
#     """ Main page/Product list """
#     queryset = Product.objects.all()
#     if not request.user.is_staff:
#         queryset = queryset.filter(count__gt=0)
#     return render(request, 'home_products_list.html', {'products': queryset})
# class ProductHomeListView(View):
#     """ Main page/Product list """
#
#     def get(self, request, *args, **kwargs):
#         queryset = Product.objects.all()
#         if not request.user.is_staff:
#             queryset = queryset.filter(count__gt=0)
#         return render(request, 'home_products_list.html', {'products': queryset})


class ProductHomeListView(View):
    """ Main page/Product list """

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all().order_by('-created_at')

        if not request.user.is_staff:
            queryset = queryset.filter(count__gt=0)
        paginator = Paginator(queryset, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'home_products_list.html', {'page_obj': page_obj})


class CancelProduct(TemplateView):
    template_name = 'cancel.html'


@csrf_exempt
def payment_pro(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.count < 1:
        # messages.error(request, 'Sorry, this product is currently out of stock.')
        # return redirect('error')
        error_url = reverse('cancel_purchase')  # , kwargs={'description': 'Product count is less than 1'})
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
        "stripe_public_key": settings.STRIPE_PUBLIC_KEY
    }
    return render(request, "payment.html", context)

# test card
# Visa: 4242 4242 4242 4242
# Mastercard: 5105 1051 0510 5100
# American Express: 3782 822463 10005
# Discover: 6011 1111 1111 1117
