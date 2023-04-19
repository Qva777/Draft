import stripe
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.http import JsonResponse

from django.shortcuts import get_object_or_404, redirect, render
from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


class CartMixin:
    """ Mixin to get the cart based on user authentication """

    @staticmethod
    def get_cart(request):
        if request.user.is_authenticated:
            return Cart.objects.get_or_create(user=request.user)[0]
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.cycle_key()
            return Cart.objects.get_or_create(session_key=session_key)[0]


class AddToCartView(View, CartMixin):
    """ Add a product to the cart """

    def get(self, request, product_id):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, id=product_id)

        quantity = int(request.POST.get('quantity', 1))
        if quantity > product.count:
            quantity = product.count

        cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
        cart_product.quantity += quantity
        cart_product.save()

        return redirect('cart_detail')


class UpdateCartView(View, CartMixin):
    """ Update the cart """

    def post(self, request, product_id):
        cart = self.get_cart(request)
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


class RemoveCartView(View, CartMixin):
    """ Remove a product from the cart """

    def get(self, request, product_id):
        cart = self.get_cart(request)
        product = get_object_or_404(Product, pk=product_id)
        cart_product = CartProduct.objects.get(cart=cart, product=product)
        cart_product.delete()
        return redirect('cart_detail')

    def post(self, request, product_id):
        return self.get(request, product_id)


class EmptyCartView(View, CartMixin):
    """ Remove all products from the cart """

    def get(self, request):
        cart = self.get_cart(request)
        cart_products = CartProduct.objects.filter(cart=cart)
        cart_products.delete()
        return redirect('cart_detail')


class CartDetailView(View, CartMixin):
    """ Display the cart contents """

    def get(self, request):
        cart = self.get_cart(request)
        cart_products = CartProduct.objects.filter(cart=cart).order_by('-created_at')

        for cart_product in cart_products:
            if cart_product.product.count == 0 or cart_product.quantity > cart_product.product.count:
                cart_product.delete()

        return render(request, 'cart_detail.html', {'cart': cart, 'cart_products': cart_products})


class PaymentCartView(View, CartMixin):
    """ Processing the cart payment """

    def post(self, request):
        cart = self.get_cart(request)
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
                'cart_id': str(cart.id)
            }
        )

        request.session['checkout_session_id'] = checkout_session.id
        request.session['cart_id'] = str(cart.id)
        request.session.modified = True

        return redirect(checkout_session.url)


class ClearCartAndDeductProductsView(View):
    """ Clear the cart after successful payment """

    @staticmethod
    def clear_cart_and_deduct_products(cart_id):
        cart = Cart.objects.get(id=cart_id)
        cart_products = CartProduct.objects.filter(cart=cart)

        for cart_product in cart_products:
            product = cart_product.product
            product.count -= cart_product.quantity
            product.save()

        cart_products.delete()

    def post(self, request):
        cart_id = request.POST.get('cart_id')
        self.clear_cart_and_deduct_products(cart_id)
        return redirect('payment_success')


class PaymentSuccessView(View, CartMixin):
    """ Successful payment cart """

    @staticmethod
    def get(request):
        if 'checkout_session_id' in request.session and 'cart_id' in request.session:
            cart_id = request.session['cart_id']
            ClearCartAndDeductProductsView.clear_cart_and_deduct_products(cart_id)
            del request.session['checkout_session_id']
            del request.session['cart_id']
            request.session.modified = True
            return render(request, "pages/payment_success.html")
        else:
            return redirect(reverse('404'))
