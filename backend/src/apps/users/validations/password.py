from django.core.validators import EmailValidator
from rest_framework import serializers
from apps.users.models import User, PasswordReset, EmailReset
from django.contrib.auth.hashers import check_password


def custom_validate_password(password):
    # TODO: Добавить валидацию перед продом
    return password


def custom_validate_password_login(data):
    password = data.get('password')
    email = data.get('email')
    username = data.get('username')

    if not password:
        raise serializers.ValidationError({"password": "Пожалуйста, введите ваш пароль."})

    if email:
        user = User.objects.filter(email=email).first()
        if user and not check_password(password, user.password):
            raise serializers.ValidationError({"password": "Неверный пароль."})

    if username:
        user = User.objects.filter(username=username).first()
        if user and not check_password(password, user.password):
            raise serializers.ValidationError({'password': 'Неверный пароль'})


# Валидация запроса сброса пароля
def custom_validate_reset_request_password(data):
    email = data.get("email")
    if not email:
        raise serializers.ValidationError({'email': 'Пожалуйста, укажите почту.'})

    user = User.objects.filter(email=email).first()
    if not user:
        raise serializers.ValidationError({'email': 'Пользователя с данной почтой не существует.'})
    if not user.is_active and not user.email_confirmed:
        raise serializers.ValidationError({'email': 'Подтвердите почту, чтобы затем сменить пароль.'})


# Валидация сброса пароля
def custom_validate_reset_verify_password(data, url):
    if not url:
        raise serializers.ValidationError({'url': 'Пожалуйста, укажите URL для сброса пароля.'})
    if not PasswordReset.objects.filter(url=url).exists():
        raise serializers.ValidationError({'url': 'Неверный URL для сброса пароля.'})
    data['url'] = url

    code = data.get('code')
    if code is None:
        raise serializers.ValidationError({'code': 'Код подтверждения обязателен.'})
    if not isinstance(code, int):
        raise serializers.ValidationError({'code': 'Код подтверждения должен быть числом.'})
    if not (100000 <= code <= 999999):
        raise serializers.ValidationError({'code': 'Код должен быть шестизначным.'})
    if not PasswordReset.objects.filter(code=code, url=url).exists():
        raise serializers.ValidationError({'code': 'Неверный код подтверждения для почты.'})

    reset = PasswordReset.objects.filter(code=code, url=url).first()
    if reset.is_expired():
        reset.delete()
        raise serializers.ValidationError({'code': "Токен сброса пароля истек."})

    password = data.get('password')
    if not password:
        raise serializers.ValidationError({'password': 'Пожалуйста, заполните поле пароля.'})

    custom_validate_password(password)


# Валидация сброса пароля
def custom_validate_reset_verify_email(data, url):
    if not url:
        raise serializers.ValidationError({'url': 'Пожалуйста, укажите URL для сброса пароля.'})
    if not EmailReset.objects.filter(url=url).exists():
        raise serializers.ValidationError({'url': 'Неверный URL для сброса пароля.'})
    data['url'] = url

    code = data.get('code')
    if code is None:
        raise serializers.ValidationError({'code': 'Код подтверждения обязателен.'})
    if not isinstance(code, int):
        raise serializers.ValidationError({'code': 'Код подтверждения должен быть числом.'})
    if not (100000 <= code <= 999999):
        raise serializers.ValidationError({'code': 'Код должен быть шестизначным.'})
    if not EmailReset.objects.filter(code=code, url=url).exists():
        raise serializers.ValidationError({'code': 'Неверный код подтверждения для почты.'})

    reset = EmailReset.objects.filter(code=code, url=url).first()
    if reset.is_expired():
        reset.delete()
        raise serializers.ValidationError({'code': "Токен сброса пароля истек."})

    email = data.get('email')
    if not email:
        raise serializers.ValidationError({'password': 'Пожалуйста, заполните поле пароля.'})

    validator = EmailValidator()
    validator(email)
