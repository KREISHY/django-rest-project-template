from datetime import timedelta
from django.db import models
from django.utils import timezone
from .users import User

from config import EMAIL_VERIFY_TOKEN_LIFETIME, PASSWORD_RESET_TOKEN_LIFETIME
from utils import generate_random_code, generate_uuid


class EmailVerify(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    code = models.IntegerField(default=generate_random_code)
    url = models.CharField(default=generate_uuid, editable=False, max_length=36)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        expiration_time = timedelta(hours=EMAIL_VERIFY_TOKEN_LIFETIME)
        return timezone.now() > self.created_date + expiration_time

    def __str__(self):
        return f"Токен подтверждения почты: {User.objects.get(pk=self.pk).email}"

    class Meta:
        verbose_name = "Токен-верификации почты"
        verbose_name_plural = "Токены-верификации почты"


class PasswordReset(models.Model):
    email = models.EmailField(unique=True)
    code = models.IntegerField(default=generate_random_code)
    url = models.CharField(default=generate_uuid, editable=False, max_length=36)
    created_date = models.DateTimeField(auto_now_add=True)

    def is_expired(self) -> bool:
        expiration_time = timedelta(hours=PASSWORD_RESET_TOKEN_LIFETIME)
        return timezone.now() > self.created_date + expiration_time

    class Meta:
        verbose_name = "Токен-сброс почты"
        verbose_name_plural = "Токены-сброса почты"
