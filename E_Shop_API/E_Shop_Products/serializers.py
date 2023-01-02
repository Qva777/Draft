from .models import Product
from rest_framework import serializers


class ProductListSerializers(serializers.ModelSerializer):
    """Serializer which return Product list 'products/' """

    # users = UserListSerializers(read_only=True, many=True)
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'photo', 'price', 'count', 'created_at', 'updated_at', 'active')


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer which CRUD Product  'products/', 'product/<int:pk>/' """

    class Meta:
        model = Product
        fields = '__all__'
        # ['id', 'name', 'description', 'photo', 'price', 'count', 'created_at', 'updated_at', 'active', ]

    def validate_count(self, value):
        """ Validator for product count """
        if value < 0:
            raise serializers.ValidationError('Product count cannot be negative.')
        elif value == 0:
            self.instance.active = False
        else:
            self.instance.active = True
        return value
