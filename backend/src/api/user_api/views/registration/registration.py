from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.users.serializers.registration import UserRegistrationsSerializer


class UserRegistrationModelViewSet(viewsets.ModelViewSet):
    """
    Регистрация пользователя
    """
    serializer_class = UserRegistrationsSerializer
    queryset = User.objects.none()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': 'success',
                    'message': 'Вы успешно зарегистрировались, пожалуйста, проверьте почту',
                },
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
