import uuid
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from apps.users.validations.user import custom_validate_user_login
from config import URL_EMAIL_VERIFY, ROOT_URL, URL_USERS_API, URL_EMAIL_RESET_VERIFY
from apps.users.models import User, EmailVerify, PasswordReset, EmailReset
from utils import generate_random_password, generate_uuid
from apps.users.validations import custom_validate_register, custom_validate_token, \
    custom_validate_reset_request_password, custom_validate_reset_verify_email


class EmailResetRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailReset
        fields = ['email']
        extra_kwargs = {
            "email": {
                'required': True,
                "error_messages": {
                    "required": "Пожалуйста, напишите вашу почту.",
                    "blank": "Пожалуйста, напишите вашу почту.",
                    "invalid": "Пожалуйста, введите корректный адрес почты.",
                }
            },
        }

    def create(self, validated_data):
        EmailReset.objects.filter(email=validated_data['email']).delete()
        reset_token = EmailReset.objects.create(email=validated_data['email'])
        EmailMessage(
            'Сброс пароля',
            f'URL: {ROOT_URL + URL_USERS_API + URL_EMAIL_RESET_VERIFY}{reset_token.url}\n{reset_token.code}',
            to=[reset_token.email]
        ).send()
        return reset_token

    def validate(self, data):
        custom_validate_reset_request_password(data)
        return data


class EmailResetVerifySerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True, required=True, error_messages={
        "required": "Пожалуйста, напишите свою почту.",
        "blank": "Пожалуйста, напишите свою почту."
    })

    class Meta:
        model = EmailReset
        fields = ['code', 'email']
        extra_kwargs = {
            "code": {
                "error_messages": {
                    "required": "Пожалуйста, напишите код.",
                    "blank": "Пожалуйста, напишите код."
                }
            },
        }

    def validate(self, data):
        url = self.context.get('url')
        custom_validate_reset_verify_email(data, url)
        return data

    def create(self, validated_data):
        reset = get_object_or_404(EmailReset, url=validated_data['url'])
        user = get_object_or_404(User, email=reset.email)
        user.email = validated_data['email']
        user.save()
        reset.delete()
        return user
