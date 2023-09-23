import random

from rest_framework import serializers

from accounts.models import UserAccount, UserPassportVerificationImages


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    inn = serializers.CharField(required=True, min_length=14, max_length=14)
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
    passport_front = serializers.ImageField(required=True)
    passport_back = serializers.ImageField(required=True)
    passport_selfie = serializers.ImageField(required=True)
    is_verified = serializers.BooleanField(read_only=True)
    user = serializers.SlugRelatedField(slug_field="full_name", read_only=True)

    class Meta:
        model = UserPassportVerificationImages
        fields = "__all__"
