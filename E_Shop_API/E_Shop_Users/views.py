from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.http import JsonResponse

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from E_Shop_API.E_Shop_Users import serializers
from E_Shop_API.E_Shop_Users.models import Clients


class UserDetailView(APIView):
    """ User Detail View get/put/patch/delete """
    permission_classes = [permissions.IsAdminUser, ]

    @staticmethod
    def get(request, pk):
        """ GET Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = serializers.UserDetailSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        """ PUT Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = serializers.MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    @staticmethod
    def patch(request, pk):
        """ PATCH Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = serializers.MyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    @staticmethod
    def delete(request, pk):
        """ DELETE/HIDE Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({'message': 'User deactivated'}, status=status.HTTP_200_OK)
        return Response({'message': 'User is already deactivate'}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def post(request, pk):
        """ Activate a disabled user """
        user = Clients.objects.get(pk=pk)
        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({'message': 'User activated'}, status=status.HTTP_200_OK)
        return Response({'message': 'User is already active'}, status=status.HTTP_400_BAD_REQUEST)


class MyUserView(APIView):
    """ Information about my user 'auth/users/me' """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """ GET Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = serializers.UserDetailSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request):
        """ PUT Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = serializers.MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request):
        """ PATCH Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = serializers.MyUserSerializer(get_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @classmethod
    def delete(cls, request):
        """ HIDE Method user 'auth/users/me/' """
        user = request.user
        if user.is_active:
            user.is_active = False
            user.save()
            return Response({'message': 'User deactivated'}, status=status.HTTP_200_OK)
        return Response({'message': 'User is already deactivated'}, status=status.HTTP_400_BAD_REQUEST)


# GOOGLE OAUTH PROVIDER
class SiteView(RetrieveUpdateAPIView):
    """ Domain site """
    permission_classes = [permissions.IsAdminUser, ]

    queryset = Site.objects.all()
    serializer_class = serializers.SiteSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """ Update site """
        site = Site.objects.get(pk=kwargs['pk'])
        site.domain = request.data.get('domain')
        site.name = request.data.get('name')
        site.save()
        return Response(serializers.SiteSerializer(site).data)


class SelectSocialApplicationView(APIView):
    """ GOOGLE OAUTH PROVIDER """
    permission_classes = [permissions.IsAdminUser, ]

    @staticmethod
    def get(request, pk):
        """ Retrieve a social app by ID """
        try:
            social_app = SocialApp.objects.get(pk=pk)
            serializer = serializers.SocialAppSerializer(social_app)
            return Response(serializer.data)
        except SocialApp.DoesNotExist:
            return Response({"error": "Social application with id {} does not exist".format(pk)})

    @staticmethod
    def post(request, pk):
        """ Create a social app with provided data """
        serializer = serializers.SocialAppSerializer(data=request.data)
        if serializer.is_valid():
            social_app = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
