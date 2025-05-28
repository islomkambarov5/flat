import random

from django.contrib.auth import login
from flat import settings
from rest_framework.decorators import permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status, serializers
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail

from .models import User
from .serializers import UserLoginSerializer, UserRegisterSerializer, PasswordChangeSerializer, \
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer, UserInfoChangeSerializer


# Create your views here.


@permission_classes([AllowAny])
class LogInApiView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, *args, **kwargs):
        serializer = UserLoginSerializer(data=self.request.data, context={'request': self.request})

        # Validate input data
        serializer.is_valid(raise_exception=True)
        # if not serializer.is_valid():
        #     return Response(
        #         {
        #             'status': 'error',
        #             'code': status.HTTP_400_BAD_REQUEST,
        #             'errors': serializer.errors
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # Authenticate user
        user = serializer.validated_data['user']
        if not user:
            return Response(
                {
                    'status': 'error',
                    'code': status.HTTP_401_UNAUTHORIZED,
                    'message': 'Invalid email or password'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Login and generate tokens
        login(self.request, user)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_200_OK)


@permission_classes([AllowAny])
class RegisterView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'code': status.HTTP_400_BAD_REQUEST,
                    'errors': serializer.errors,
                    'message': 'Registration failed. Please correct the errors below.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = serializer.save()
            return Response(
                {
                    'status': 'success',
                    'code': status.HTTP_201_CREATED,
                    'message': 'User created successfully.',
                    'user': {
                        'id': user.id,
                        'email': user.email,
                        'username': user.username
                    }
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {
                    'status': 'error',
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'An error occurred during registration.',
                    'error': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@permission_classes([IsAuthenticated])
class PasswordChangeApiView(GenericAPIView):
    serializer_class = PasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Password updated successfully",
            "data": {
                "email": user.email,
                "username": user.username
            }
        })


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        user = User.objects.get(email=email)

        # Generate token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Send email (in production, use Celery for this)
        reset_url = f"{settings.FRONTEND_URL}/api/user/password-reset/confirm/{uid}/{token}/"
        send_mail(
            'Password Reset Request',
            f'Click the link to reset your password: {reset_url}'
            f'uid: {uid}'
            f'token: {token}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        return Response(
            {"detail": "Password reset link has been sent to your email.",
             'url': reset_url},
            status=status.HTTP_200_OK
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"uid": "Invalid user ID"})

        token_generator = PasswordResetTokenGenerator()
        if not token_generator.check_token(user, serializer.validated_data['token']):
            raise serializers.ValidationError({"token": "Invalid or expired token"})

        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK
        )


@permission_classes([IsAuthenticated])
class UserInfoChangeView(GenericAPIView):
    serializer_class = UserInfoChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

