from rest_framework import permissions
from E_Shop_API.E_Shop_Products.serializers import ProductSerializer

from django.http import JsonResponse
import stripe
from django.conf import settings

from E_Shop_API.E_Shop_Products.models import Product

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCreateView(APIView):
    """ Create Product """
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        """ Create product """
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class ProductListView(APIView):
    """ Info about all product '/api/products/' """
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request, format=None):
        """ Filer for Product queryset """
        queryset = Product.objects.all()
        if not request.user.is_staff:
            queryset = queryset.filter(count__gt=0)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class ProductView(APIView):
    permission_classes = [permissions.IsAdminUser]

    @staticmethod
    def get(request, pk, format=None):
        """ GET Method product/<int:pk>/ """
        product = Product.objects.get(pk=pk)
        if not request.user.is_staff and product.count == 0:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk, format=None):
        """ PUT Method product/<int:pk>/ """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def patch(request, pk):
        """ PATCH Method product/<int:pk>/ """
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @staticmethod
    def delete(request, pk):
        """ DELETE Method product/<int:pk>/ """
        product = Product.objects.get(pk=pk)
        product.delete()
        return Response(status=204)




#
# def payment_pro(request, product_id):
#     """ checkout """
#
#     product = Product.objects.get(id=product_id)
#     if product.count < 1:
#         raise ValueError("Products are not enough")
#
#
#     product.count -= 1
#     product.save()
#
#     checkout_session = stripe.checkout.Session.create(
#         # payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': product.name,
#                         'description': product.description,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url='http://127.0.0.1:8000/api/success_pro/',
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#     )
#
#     # Add the product_id to the checkout session metadata
#     checkout_session['metadata']['product_id'] = product_id
#
#     request.session['checkout_session_id'] = checkout_session.id
#     request.session['product_id'] = product_id
#
#     # store the checkout session id and product_id in the cache
#     cache.set('checkout_session_id', checkout_session.id, timeout=60)
#     cache.set('product_id', product_id, timeout=60)
#
#     return redirect(checkout_session.url)
#
# def return_product(request):
#     # Retrieve the product_id from the cache
#     product_id = cache.get(product_id)
#     if product_id:
#         # Return the product to the inventory
#         product = Product.objects.get(id=product_id)
#         product.count += 1
#         product.save()
#         # Delete the product_id from the cache
#         cache.delete(product_id)
#     return redirect('home_products_list')
#
#
# def success_pro(request):
#     # the payment was successful, so delete the cache entries
#     cache.delete('checkout_session_id')
#     cache.delete('product_id')
#
#     # redirect the user to a success page
#     return redirect('success')
#
#
# def cancel_pro(request):
#     checkout_session_id = cache.get('checkout_session_id')
#     product_id = cache.get('product_id')
#
#     # if the checkout session id or product id are not in the cache, then do nothing
#     if not checkout_session_id or not product_id:
#         return
#
#     # the payment was cancelled, so return the product
#     product = Product.objects.get(id=product_id)
#     product.count += 1
#     product.save()
#
#     # delete the cache entries
#     cache.delete('checkout_session_id')
#     cache.delete('product_id')
#
#     return redirect('home_products_list')


# def payment_pro(request, product_id):
#     """ checkout """
#
#     product = Product.objects.get(id=product_id)
#     if product.count < 1:
#         raise ValueError("Products are not enough")
#
#     # decrement the product count
#     # product.count -= 1
#     # product.save()
#
#     # create the checkout session with Stripe
#     checkout_session = stripe.checkout.Session.create(
#         # payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': product.name,
#                         'description': product.description,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url='http://127.0.0.1:8000/api/success_pro/',
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#     )
#
#     # add the product_id to the checkout session metadata
#     checkout_session['metadata']['product_id'] = product_id
#     request.session['checkout_session_id'] = checkout_session.id
#     request.session['product_id'] = product_id
#     # store the checkout session id and product_id in the cache
#     # Schedule the return_product_after_30_seconds task
#
#     return redirect(checkout_session.url)
# def payment_pro(request, product_id):
#     """ checkout """
#
#     product = Product.objects.get(id=product_id)
#     if product.count < 1:
#         raise ValueError("Products are not enough")
#
#     # decrement the product count
#     # product.count -= 1
#     # product.save()
#
#     # create the checkout session with Stripe
#     checkout_session = stripe.checkout.Session.create(
#         # payment_method_types=['card'],
#         line_items=[
#             {
#                 'price_data': {
#                     'currency': 'usd',
#                     'product_data': {
#                         'name': product.name,
#                         'description': product.description,
#                     },
#                     'unit_amount': int(product.price * 100),
#                 },
#                 'quantity': 1,
#             },
#         ],
#         mode='payment',
#         success_url='http://127.0.0.1:8000/api/success_pro/',
#         cancel_url=request.build_absolute_uri(reverse('cancel')),
#     )
#
#     # add the product_id to the checkout session metadata
#     checkout_session['metadata']['product_id'] = product_id
#     request.session['checkout_session_id'] = checkout_session.id
#     request.session['product_id'] = product_id
#
#
#     return redirect(checkout_session.url)


# def payment_pro(request, product_id):
#     # Get the product object
#     product = get_object_or_404(Product, id=product_id)
#
#     # Check if there are enough products available
#     if product.count <= 0:
#         messages.error(request, 'Sorry, this product is currently out of stock.')
#         return redirect('product_detail', product_id=product.id)
#
#     # Handle the payment
#     if request.method == 'POST':
#         try:
#             charge = stripe.Charge.create(
#                 amount=int(product.price * 100),  # Amount in cents
#                 currency='usd',
#                 source=request.POST['stripeToken'],
#                 description=product.name
#             )
#             # Update the product count and save it
#             product.count -= 1
#             product.save()
#             messages.success(request, 'Your payment was successful.')
#             return redirect('product_detail', product_id=product.id)
#         except stripe.error.CardError as e:
#             messages.error(request, 'Your payment could not be processed. Please try again or contact your bank.')
#     else:
#         # Render the payment form
#         context = {
#             'product': product,
#             'stripe_public_key': settings.STRIPE_PUBLIC_KEY
#         }
#         return render(request, 'payment.html', context)



# preparing to delete
# @csrf_exempt
# def payment_pro(request, product_id):
#     product = get_object_or_404(Product, id=product_id)
#     if product.count < 1:
#         # messages.error(request, 'Sorry, this product is currently out of stock.')
#         # return redirect('error')
#         error_url = reverse('home')#, kwargs={'description': 'Product count is less than 1'})
#         return redirect(error_url)
#     if request.method == "POST":
#         # Use Stripe to charge the user's card
#         token = request.POST.get("stripeToken")
#         amount = int(product.price * 100)
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
#         # Update the product quantity
#         product.count -= 1
#         product.save()
#
#         # Return the updated product quantity in the response
#         return JsonResponse({"quantity": product.count})
#
#     context = {
#         "product": product,
#         "stripe_public_key": settings.STRIPE_PUBLIC_KEY
#     }
#     return render(request, "payment.html", context)
