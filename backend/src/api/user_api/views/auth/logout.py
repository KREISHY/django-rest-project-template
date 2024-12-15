from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.users.serializers.login import UserLoginByEmailSerializer


class UserLogoutViewSet(viewsets.ViewSet):
    """
    Выход из системы
    """
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options', 'list']

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return Response(
                {'status': 'success', 'message': 'Вы успешно вышли из системы'},
                status=status.HTTP_204_NO_CONTENT
            )

        return Response(
            {'status': 'error', 'message': 'Пользователь не авторизирован или уже вышел из системы'},
            status=status.HTTP_401_UNAUTHORIZED
        )