import base64
import random

from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer

from accounts.models import UserAccount, UserPassportVerificationImages


class TokenObtainLifetimeSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['auth_status'] = user.auth_status
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['access_token_lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        data['refresh_token_lifetime'] = int(refresh.lifetime.total_seconds())
        data['auth_status'] = self.user.auth_status
        data['id'] = self.user.id
        data['full_name'] = self.user.full_name
        data['email'] = self.user.email
        data['inn'] = self.user.inn
        data['name'] = self.user.name
        return data


class TokenRefreshLifetimeSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    def validate_refresh(self, value):
        if value == "" or value is None:
            return Response({"message": "Refresh token is required."}, status=status.HTTP_401_UNAUTHORIZED)
        return value


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    inn = serializers.CharField(required=True, max_length=14)
    password = serializers.CharField(required=True, min_length=8)
    full_name = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value

    def validate_inn(self, value):
        if UserAccount.objects.filter(inn=value).exists():
            raise serializers.ValidationError("Пользователь с таким ИНН уже существует.")
        return value


class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)

    def validate_email(self, value):
        if UserAccount.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует.")
        return value


class UserPassportVerificationImagesSerializer(serializers.ModelSerializer):
    passport_front = Base64ImageField(required=True)
    passport_selfie = Base64ImageField(required=True)
    is_verified = serializers.BooleanField(read_only=True)
    user = serializers.SlugRelatedField(slug_field="full_name", read_only=True)

    class Meta:
        model = UserPassportVerificationImages
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        refresh = TokenObtainPairSerializer.get_token(self.user)

        data['access_token_lifetime'] = int(refresh.access_token.lifetime.total_seconds())
        data['refresh_token_lifetime'] = int(refresh.lifetime.total_seconds())
        data['auth_status'] = self.user.auth_status
        data['id'] = self.user.id
        data['full_name'] = self.user.full_name
        data['email'] = self.user.email
        data['inn'] = self.user.inn
        data['name'] = self.user.name
        data['access_token']: str(refresh.access_token)
        data['refresh']: str(refresh)
        return data


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        exclude = (
            "password",
            "groups",
            "user_permissions",
            "is_staff",
            "is_superuser",
            "is_active",
            "last_login",
            "date_joined",
        )
