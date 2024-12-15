import re
from rest_framework import serializers
from apps.users.models import User


def custom_validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise serializers.ValidationError({'email': 'Введите корректный адрес электронной почты.'})

    forbidden_domains = ['tempmail.com', 'example.com']
    domain = email.split('@')[1]
    if domain in forbidden_domains:
        raise serializers.ValidationError({'email': 'Использование этих почтовых сервисов запрещено.'})
    return email


def custom_validate_password(password):
    # TODO: Добавить валидацию перед продом
    return password


def custom_validate_first_name(first_name):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", first_name):
        raise serializers.ValidationError({'first_name': 'Имя должно содержать только буквы.'})
    return first_name


def custom_validate_last_name(last_name):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", last_name):
        raise serializers.ValidationError({'last_name': 'Фамилия должна содержать только буквы.'})
    return last_name


def custom_validate_patronymic(patronymic):
    if not re.match(r"^[а-яА-ЯёЁa-zA-Z]+$", patronymic):
        raise serializers.ValidationError({'patronymic': 'Отчество должно содержать только буквы.'})
    return patronymic


# Валидация регистрации
def custom_validate_register(data):
    email = data.get('email')
    if not email:
        raise serializers.ValidationError({'email': 'Пожалуйста, заполните поле почты.'})
    if User.objects.filter(email=email).exists():
        raise serializers.ValidationError({'email': 'Эта почта уже используется.'})
    custom_validate_email(email)

    password = data.get('password')
    if not password:
        raise serializers.ValidationError({'password': 'Пожалуйста, заполните поле пароля.'})
    custom_validate_password(password)

    last_name = data.get('last_name')
    if not last_name:
        raise serializers.ValidationError({'last_name': 'Пожалуйста, заполните поле фамилии.'})
    custom_validate_last_name(last_name)

    first_name = data.get('first_name')
    if not first_name:
        raise serializers.ValidationError({'first_name': 'Пожалуйста, заполните поле имени.'})
    custom_validate_first_name(first_name)

    patronymic = data.get('patronymic')
    if patronymic:
        custom_validate_patronymic(patronymic)
