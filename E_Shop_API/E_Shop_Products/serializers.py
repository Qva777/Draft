from .models import Product
from rest_framework import serializers


class ProductListSerializers(serializers.ModelSerializer):
    """Serializer which return Product list 'products/' """

    # users = UserListSerializers(read_only=True, many=True)
    class Meta:
        model = Product
        fields = '__all__'
        # fields = ('id', 'name', 'description', 'price', 'count', 'created_at', 'updated_at', 'active')


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer which CRUD Product  'products/', 'product/<int:pk>/' """

    class Meta:
        model = Product
        fields = '__all__'
        # ['id', 'name', 'description', 'photo', 'price', 'count', 'created_at', 'updated_at', 'active', ]