from .serializers import CustomUserRegistrationSerializer, LoginSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import CustomUser
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status


class CustomUserRegistrationView(CreateAPIView):
    serializer_class = CustomUserRegistrationSerializer

    def perform_create(self, serializer):
        serializer.save()


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer