from django.urls import path
from rest_framework.routers import DefaultRouter
from api.user_api.views.auth import (
    LoginByEmailViewSet, CurrentUserViewSet,
    UserLogoutViewSet,
)
from api.user_api.views.registration import (
    UserRegistrationModelViewSet,
    EmailTokenConfirmationView,
)
from api.user_api.views.reset import (
    ResetPasswordConfirmationView,
    ResetPasswordRequestView,
    ResetEmailConfirmationView,
    ResetEmailRequestView
)
from config.config import (
    URL_EMAIL_VERIFY, URL_PASSWORD_RESET_VERIFY, URL_EMAIL_RESET_VERIFY
)

email_verify_url = URL_EMAIL_VERIFY.replace("/", "")
password_reset_confirm_url = URL_PASSWORD_RESET_VERIFY.replace("/", "")
email_reset_confirm_url = URL_EMAIL_RESET_VERIFY.replace("/", "")


router = DefaultRouter()
router.register(r'login', LoginByEmailViewSet, basename='login')
router.register(r'current-user', CurrentUserViewSet, basename='current-user')
router.register(r'logout', UserLogoutViewSet, basename='logout')
router.register(r'register', UserRegistrationModelViewSet, basename='register')
router.register(email_verify_url, EmailTokenConfirmationView, basename=email_verify_url)
router.register(r'password-reset-create', ResetPasswordRequestView, basename='password-reset-create')
router.register(password_reset_confirm_url, ResetPasswordConfirmationView, basename=password_reset_confirm_url)
router.register(r'email-reset-create', ResetEmailRequestView, basename='email-reset-create')
router.register(email_reset_confirm_url, ResetEmailConfirmationView, basename=email_reset_confirm_url)


urlpatterns = []
urlpatterns += router.urls