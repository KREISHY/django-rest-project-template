from rest_framework import serializers
from apps.users.models import EmailVerify


# Валидация токенов
def custom_validate_token(data, url):
    custom_validate_email_token_url(url)
    custom_validate_email_token_code(data, url)


def custom_validate_email_token_url(url):
    if not url:
        raise serializers.ValidationError({'url': 'Пожалуйста, укажите URL подтверждения.'})
    if not EmailVerify.objects.filter(url=url).exists():
        raise serializers.ValidationError({'url': 'Неверный URL подтверждения.'})


def custom_validate_email_token_code(data, url):
    code = data.get('code')
    if code is None:
        raise serializers.ValidationError({'code': "Поле 'code' обязательно для заполнения."})
    if not isinstance(code, int):
        raise serializers.ValidationError({'code': "Поле 'code' должно быть числом."})
    if not (100000 <= code <= 999999):
        raise serializers.ValidationError({'code': "Код должен быть шестизначным."})

    token = EmailVerify.objects.filter(code=code, url=url).first()
    if not token:
        raise serializers.ValidationError({'code': "Неверный код подтверждения."})

    if token.is_expired():
        token.user.delete()
        token.delete()
        raise serializers.ValidationError({'code': "Токен подтверждения истек."})

    if token.user.is_active:
        raise serializers.ValidationError({'code': "Почта уже подтверждена."})