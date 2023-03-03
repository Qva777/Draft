

# from E_Shop_API.E_Shop_Users.models import Clients
#
# from E_Shop_API.E_Shop_Cart.models import Cart, CartProduct
# from rest_framework import serializers
#
#
# # class UserSerializer(serializers.ModelSerializer):
# #     """ User Serializer """
# #     class Meta:
# #         model = Clients
# #         fields = ('id', 'email')
# #
# # class CartSerializer(serializers.ModelSerializer):
# #     """ Post/Get Cart """
# #     user = UserSerializer(read_only=True)
# #
# #     class Meta:
# #         model = Cart
# #         fields = ('id', 'user', 'created_at', 'total_price')
#
#
# class CartSerializer(serializers.ModelSerializer):
#     """ Post/Get/ Cart"""
#
#     class Meta:
#         model = Cart
#         fields = ('id', 'user', 'created_at', 'total_price')
#
#
# class CartProductSerializer(serializers.ModelSerializer):
#     """ Adds Product into Cart model """
#
#     class Meta:
#         model = CartProduct
#         fields = ('id', 'quantity',)
#
#
# class GetUserSerializer(serializers.ModelSerializer):
#     """ Get username """
#
#     class Meta:
#         model = Clients
#         fields = ('username',)
#
#
# class GetCartUserSerializer(serializers.ModelSerializer):
#     """ Get user """
#     user = GetUserSerializer(read_only=True)
#
#     class Meta:
#         model = Cart
#         fields = ('user',)
#
#
# class CartProductDetailSerializer(serializers.ModelSerializer):
#     """ Show Detail view about CartProduct """
#     cart = GetCartUserSerializer(read_only=True)
#     product = serializers.CharField(source='product.name')
#
#     class Meta:
#         model = CartProduct
#         fields = ('id', 'cart', 'product', 'quantity', 'price', 'total_price')
