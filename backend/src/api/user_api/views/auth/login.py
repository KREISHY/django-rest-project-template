from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, permissions, status
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from apps.users.models import User
from apps.users.serializers.login import UserLoginByEmailSerializer


class LoginByEmailViewSet(ModelViewSet):
    """
    Вход в систему
    """
    model = User
    queryset = User.objects.none
    serializer_class = UserLoginByEmailSerializer
    permission_classes = [permissions.AllowAny]
    http_method_names = ['get', 'post', 'head', 'options', 'list']

    def list(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({
                'status': 'authenticated', 'message': 'Вы уже вошли в систему'},
                status=status.HTTP_403_FORBIDDEN,
            )

        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if request.user.is_authenticated:
            return Response({
                'status': 'authenticated', 'message': 'Вы уже вошли в систему'},
                status=status.HTTP_403_FORBIDDEN,
            )

        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, email=email, password=password)
            if not user:
                return Response({'status': 'error', 'message': 'Предоставлены неверные данные'},
                                status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            return Response(
                {'status': 'ok', 'message': 'Вы успешно вошли в систему'},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
