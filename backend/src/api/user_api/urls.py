from django.urls import path
from rest_framework.routers import DefaultRouter
from api.user_api.views.auth import (
    LoginByEmailViewSet, CurrentUserViewSet,
    UserLogoutViewSet,
)

router = DefaultRouter()
router.register(r'login', LoginByEmailViewSet, basename='login')
router.register(r'current-user', CurrentUserViewSet, basename='current-user')
router.register(r'logout', UserLogoutViewSet, basename='logout')

urlpatterns = []
urlpatterns += router.urls