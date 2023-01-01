from .models import User_manager
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserDetailSerializer(serializers.ModelSerializer):
    """Return fields in  GET user detail """

    class Meta:
        model = User_manager
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'birth_date', 'photo', 'disabled',
                  'created_at', 'updated_at']


class MyUserSerializer(serializers.ModelSerializer):
    """Return fields in  PUT/PATCH user """
    password = serializers.CharField(validators=[validate_password])

    class Meta:
        model = User_manager
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'birth_date', 'photo', 'disabled',
                  'created_at', 'updated_at', 'product']

    def update(self, instance, validated_data):
        """ HASH Password when you update it"""
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data['password'])
            user.save()
        except KeyError:
            pass
        return user
