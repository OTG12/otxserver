from rest_framework import serializers
from .models import User
from django.utils import timezone
from .backend import CustomBackend
from rest_framework_simplejwt.tokens import RefreshToken

auth_service = CustomBackend()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password', 'created_at', 'updated_at']
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        if password:
            user.set_password(password) 
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get("request")
        email = data.get("email")
        password = data.get("password")
        if not email:
            raise serializers.ValidationError("Email required.")
        if not password:
            raise serializers.ValidationError("Password required.")
        user = auth_service.authenticate(request, email=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials. Please try again.")
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        user.last_login = timezone.now()
        user.save()
        data["user"] = user
        return data
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "password",
            "created_at",
        ]