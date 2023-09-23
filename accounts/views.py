import random
import redis
from django.core.mail import send_mail
from decouple import config

from django.http import HttpRequest
from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer

from accounts import serializers
from accounts.models import UserAccount, UserPassportVerificationImages

redis_client = redis.StrictRedis(host='redis', port=6379, db=0)


class TokenObtainPairView(TokenViewBase):
    """
        Return JWT tokens (access and refresh) for specific user based on username and password.
    """
    serializer_class = TokenObtainPairSerializer


class TokenRefreshView(TokenViewBase):
    """
        Renew tokens (access and refresh) with new expire time based on specific user's access token.
    """
    serializer_class = TokenRefreshSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.RegisterSerializer

    def post(self, request: HttpRequest) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        verification_code = random.randint(1000, 9999)

        subject = 'Verify Your Email'
        message = f'Your verification code is {verification_code}'
        from_email = config("SEND_MAIL")  # Update this with your email
        recipient_list = [serializer.validated_data["email"]]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        print(verification_code)
        validated_data = serializer.validated_data

        redis_data = {
            'email': validated_data["email"],
            'inn': validated_data["inn"],
            'password': validated_data["password"],
            'full_name': validated_data["full_name"],
            'name': validated_data["name"],
            'verification_code': verification_code,
        }
        unique_token = validated_data['email']
        redis_client.hmset(unique_token, redis_data)
        redis_client.expire(unique_token, 120)

        return Response({"message": "Код подтверждения отправлен на вашу почту."})


class VerifyCodeView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.VerifyCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        stored_email = redis_client.hgetall(email)
        if not stored_email:
            return Response({"message": "Срок действия кода истек"}, status=status.HTTP_404_NOT_FOUND)

        stored_code = stored_email[b'verification_code'].decode('utf-8')

        if code == stored_code:
            user = UserAccount.objects.create(
                email=email,
                inn=stored_email[b'inn'].decode('utf-8'),
                password=stored_email[b'password'].decode('utf-8'),
                full_name=stored_email[b'full_name'].decode('utf-8'),
                name=stored_email[b'name'].decode('utf-8')
            )
            user.save()

            token = TokenObtainPairSerializer.get_token(user)
            data = {
                'access_token': str(token.access_token),
                'refresh': str(token),
                'access_token_expires_in': token.access_token.lifetime.total_seconds(),
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)


class UserPassportVerificationImagesView(generics.CreateAPIView):
    serializer_class = serializers.UserPassportVerificationImagesSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        user = self.request.user

        serializer.save(
            user=user
        )
