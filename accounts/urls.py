from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import TokenObtainPairView, TokenRefreshView, RegisterView, VerifyCodeView
from .views import UserPassportVerificationImagesView, UserMeView
router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path('auth/verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('auth/passport-images-upload/', UserPassportVerificationImagesView.as_view(), name='verify-passport-images'),
    path('auth/me/', UserMeView.as_view(), name='user-me'),
]
