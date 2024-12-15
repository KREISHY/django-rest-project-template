from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.users.serializers.login import UserLoginByEmailSerializer
from apps.users.serializers.user import UserCurrentSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    """
    Текущий пользователь
    Если пользователь не авторизирован указывает пустые поля
    """
    serializer_class = UserCurrentSerializer
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        serializer = UserCurrentSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
