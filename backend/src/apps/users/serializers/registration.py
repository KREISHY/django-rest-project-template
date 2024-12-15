from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from config import URL_EMAIL_VERIFY, ROOT_URL, URL_USERS_API
from apps.users.models import User, EmailVerify
from apps.users.validations import custom_validate_register


class UserRegistrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'last_name', 'first_name', 'patronymic', 'password']
        extra_kwargs = {
            "username": {
                "error_messages": {
                    'blank': 'Пожалуйста, укажите имя пользователя.',
                    'required': 'Пожалуйста, укажите имя пользователя.',
                }
            },

            "email": {
                "required": True,
                "error_messages": {
                    "required": "Укажите ваш email.",
                    "blank": "Пожалуйста, напишите вашу почты.",
                    "invalid": "Пожалуйста, введите корректный адрес почты.",
                }
            },
            "password": {
                "error_messages": {"required": "Введите пароль.", "blank": "Пожалуйста, напишите ваш пароль."}},
            "last_name": {
                "error_messages": {"required": "Введите фамилию.", "blank": "Пожалуйста, напишите вашу фамилию."}},
            "first_name": {
                "error_messages": {"required": "Введите имя.", "blank": "Пожалуйста, напишите ваше имя."}},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            last_name=validated_data.get('last_name', ''),
            first_name=validated_data.get('first_name', ''),
            patronymic=validated_data.get('patronymic', ''),
            is_active=False,
            username= validated_data.get('username', ''),
        )
        token = EmailVerify.objects.create(user=user)
        EmailMessage(
            'Подтверждение почты',
            f'URL: {ROOT_URL + URL_USERS_API + URL_EMAIL_VERIFY}{token.url}\n{token.code}',
            to=[user.email]
        ).send()
        return user

    def validate(self, data):
        custom_validate_register(data)
        return data

