import uuid

from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

# from config import URL_EMAIL_VERIFY, ROOT_URL, URL_USERS_API, URL_PASSWORD_RESET_VERIFY
from apps.users.models import User, EmailVerify, PasswordReset
from utils import generate_random_password, generate_uuid
from apps.users.validations import custom_validate_register, custom_validate_token, custom_validate_reset_request_password, \
    custom_validate_reset_verify_password


class UserCurrentSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'groups']

    def get_groups(self, obj):
        group_names = list(obj.groups.values_list("name", flat=True))
        if obj.is_superuser:
            group_names.append("superuser")
        return group_names