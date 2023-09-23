from rest_framework import serializers

from accounts.models import UserAccount


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    inn = serializers.CharField(required=True, min_length=14, max_length=14)
    password = serializers.CharField(required=True, min_length=8)
    full_name = serializers.CharField(required=True)
    name = serializers.CharField(required=True)

    # def validate_email(self, email):
    def create(self, validated_data):
        user = UserAccount.objects.create(
            email=validated_data["email"],
            inn=validated_data["inn"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            name=validated_data["name"],
        )
        user.save()

        return user