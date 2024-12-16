from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.users.models import EmailVerify
from apps.users.serializers.email import EmailTokenCreationSerializer


class EmailTokenConfirmationView(viewsets.ModelViewSet):
    """
    Подтверждение почты
    - Работает только если вы перешли на URL указанный в письме при регистрации
    - Требует код указанный в письме
    """
    serializer_class = EmailTokenCreationSerializer
    queryset = EmailVerify.objects.none()
    http_method_names = ['get', 'post', 'head', 'options', 'list']
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'], url_path='(?P<url>[^/.]+)')
    def confirm_email(self, request, url=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'url': url})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
