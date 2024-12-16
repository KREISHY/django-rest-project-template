from django.urls import path
from rest_framework.routers import DefaultRouter
from api.user_api.views.auth import (
    LoginByEmailViewSet, CurrentUserViewSet,
    UserLogoutViewSet, UserRegistrationModelViewSet,
    EmailTokenConfirmationView,
)
from config.config import (
    URL_EMAIL_VERIFY, URL_PASSWORD_RESET_VERIFY,
)
email_verify_url = URL_EMAIL_VERIFY.replace("/", "")


router = DefaultRouter()
router.register(r'login', LoginByEmailViewSet, basename='login')
router.register(r'current-user', CurrentUserViewSet, basename='current-user')
router.register(r'logout', UserLogoutViewSet, basename='logout')
router.register(r'register', UserRegistrationModelViewSet, basename='register')
router.register(email_verify_url, EmailTokenConfirmationView, basename=email_verify_url)


urlpatterns = []
urlpatterns += router.urls