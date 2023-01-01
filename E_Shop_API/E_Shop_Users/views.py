from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from django.http import JsonResponse

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateAPIView

from E_Shop_API.E_Shop_Users.models import Clients
from E_Shop_API.E_Shop_Users.serializers import MyUserSerializer, UserDetailSerializer, SocialAppSerializer, \
    SiteSerializer


class UserDetailView(APIView):
    """ User Detail View get/put/patch/delete """
    permission_classes = [permissions.IsAdminUser, ]

    @staticmethod
    def get(request, pk):
        """ GET Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        """ PUT Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)

    #     return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def patch(request, pk):
        """ PATCH Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        serializer = MyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        # return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def delete(request, pk):
        """ DELETE Method user/<int:pk>/ """
        user = Clients.objects.get(pk=pk)
        user.delete()
        return Response(status=204)


class MyUserView(APIView):
    """ Information about my user 'auth/users/me' """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """ GET Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = UserDetailSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request):
        """ PUT Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request):
        """ PATCH Method user 'auth/users/me/' """
        get_user = self.request.user
        user = Clients.objects.get(pk=get_user.pk)
        serializer = MyUserSerializer(get_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @classmethod
    def delete(cls, request):
        """ HIDE Method user 'auth/users/me/' """
        user = request.user
        user.is_active = False
        user.save()
        #     user.delete()
        #  return active by email
        return Response(status=204)


# GOOGLE OAUTH PROVIDER
class SiteView(RetrieveUpdateAPIView):
    """ A view to retrieve and update site details """
    permission_classes = [permissions.IsAdminUser, ]

    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        """ Update site details """
        site = Site.objects.get(pk=kwargs['pk'])
        site.domain = request.data.get('domain')
        site.name = request.data.get('name')
        site.save()
        return Response(SiteSerializer(site).data)


class SelectSocialApplicationView(APIView):
    """ A view to retrieve and create a social application """
    permission_classes = [permissions.IsAdminUser, ]

    @staticmethod
    def get(request, pk):
        """ Retrieve a social app by ID """
        try:
            social_app = SocialApp.objects.get(pk=pk)
            serializer = SocialAppSerializer(social_app)
            return Response(serializer.data)
        except SocialApp.DoesNotExist:
            return Response({"error": "Social application with id {} does not exist".format(pk)})

    @staticmethod
    def post(request, pk):
        """ Create a social app with provided data """
        serializer = SocialAppSerializer(data=request.data)
        if serializer.is_valid():
            social_app = serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
