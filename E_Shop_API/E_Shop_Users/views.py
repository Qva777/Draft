from django.http import JsonResponse

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from E_Shop_Users.models import User_manager
from E_Shop_Users.serializers import MyUserSerializer, UserDetailSerializer


class UserDetailView(APIView):
    """ User Detail View get/put/patch/delete """

    @staticmethod
    def get(request, pk):
        """ GET Method user/<int:pk>/ """
        user = User_manager.objects.get(pk=pk)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

    @staticmethod
    def put(request, pk):
        """ PUT Method user/<int:pk>/ """
        user = User_manager.objects.get(pk=pk)
        serializer = MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def patch(request, pk):
        """ PATCH Method user/<int:pk>/ """
        user = User_manager.objects.get(pk=pk)
        serializer = MyUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    @staticmethod
    def delete(request, pk):
        """ DELETE Method user/<int:pk>/ """
        user = User_manager.objects.get(pk=pk)
        user.delete()
        return Response(status=204)


class MyUserView(APIView):
    """ Information about my user 'auth/users/me' """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """ GET Method user 'auth/users/me/' """
        get_user = self.request.user
        user = User_manager.objects.get(pk=get_user.pk)
        serializer = UserDetailSerializer(user)
        return JsonResponse(serializer.data)

    def put(self, request):
        """ PUT Method user 'auth/users/me/' """
        get_user = self.request.user
        user = User_manager.objects.get(pk=get_user.pk)
        serializer = MyUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def patch(self, request):
        """ PATCH Method user 'auth/users/me/' """
        get_user = self.request.user
        user = User_manager.objects.get(pk=get_user.pk)
        serializer = MyUserSerializer(get_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    @classmethod
    def delete(self, request):
        """ DELETE Method user 'auth/users/me/' """
        user = request.user
        user.delete()
        return Response(status=204)
