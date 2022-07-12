from rest_framework import serializers
from users.models import CustomUser, UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from message.api.serializers import GenericFileUploadSerializer
from django.db.models import Q
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


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["created_date", "updated_date", "is_staff", "is_active", "groups", "user_permissions", "password", "last_login", "is_superuser"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    profile_picture = GenericFileUploadSerializer(read_only=True)
    profile_picture_id = serializers.IntegerField(write_only=True)
    message_count = serializers.SerializerMethodField('get_message_count')
    class Meta:
        model = UserProfile
        exclude = ["created_date", "updated_date"]

    def get_message_count(self, obj):
        try:
            user_id = self.context["request"].user.id
        except Exception as e:
            user_id = None

        from message.models import Message
        message = Message.objects.filter(Q(sender_id=user_id, receiver_id=obj.user.id) | Q(sender_id=obj.user.id, receiver_id=user_id)).distinct()
        return message.count()





