import uuid
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.validations.user import custom_validate_user_login
from config import URL_EMAIL_VERIFY, ROOT_URL, URL_USERS_API, URL_PASSWORD_RESET_VERIFY
from apps.users.models import User, EmailVerify, PasswordReset
from utils import generate_random_password, generate_uuid
from apps.users.validations import custom_validate_register, custom_validate_token, \
    custom_validate_reset_request_password, custom_validate_reset_verify_password


class UserLoginByEmailSerializer(ModelSerializer):
    email = serializers.EmailField(required=True, error_messages={
        "required": "Пожалуйста, напишите вашу почту.",
        "blank": "Пожалуйста, напишите вашу почту.",
        "invalid": "Пожалуйста, введите корректный адрес почты.",
    })

    password = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите ваш пароль.",
        "blank": "Пожалуйста, напишите ваш пароль.",
    })

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate(self, data):
        custom_validate_user_login(data)
        return data


class UserLoginByUsernameSerializer(ModelSerializer):
    username = serializers.CharField(required=True, error_messages={
        "required": "Пожалуйста, напишите имя пользователя.",
        "blank": "Пожалуйста, напишите имя пользователя.",
    })

    password = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите ваш пароль.",
        "blank": "Пожалуйста, напишите ваш пароль.",
    })

    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        custom_validate_user_login(data)
        return data


class UserLoginByUsernameSerializer(ModelSerializer):
    username = serializers.CharField(required=True, error_messages={
        "required": "Пожалуйста, напишите имя пользователя.",
        "blank": "Пожалуйста, напишите имя пользователя.",
    })

    password = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите ваш пароль.",
        "blank": "Пожалуйста, напишите ваш пароль.",
    })


    class Meta:
        model = User
        fields = ['username', 'password']


    def validate(self, data):
        custom_validate_user_login(data)
        return data
