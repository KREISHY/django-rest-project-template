from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import PasswordReset
from apps.users.serializers.password import PasswordResetRequestSerializer, PasswordResetVerifySerializer


class ResetPasswordRequestView(viewsets.ModelViewSet):
    """
    Восстановление пароля
    """
    serializer_class = PasswordResetRequestSerializer
    queryset = PasswordReset.objects.none()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmationView(viewsets.ModelViewSet):
    serializer_class = PasswordResetVerifySerializer
    queryset = PasswordReset.objects.none()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], url_path='(?P<url>[^/.]+)')
    def confirm_password_password_reset(self, request, url=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'url': url})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
