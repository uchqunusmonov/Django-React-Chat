from rest_framework import serializers
from users.models import CustomUser, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserRegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})

    class Meta:
        model = CustomUser
        exclude = ["is_superuser", "is_active", "groups", "user_permissions", "created_date", "updated_date", "last_login", "is_staff"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        return token

