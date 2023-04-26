from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "password",
            "phone",
            "profile_pic",
        ]

    def create(self, validated_data):
        unhashed_password = validated_data["password"]
        password = make_password(unhashed_password)
        if "profile_pic" not in validated_data:
            validated_data["profile_pic"] = "default.jpeg"
        user = User.objects.create(
            username=validated_data["username"],
            password=password,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone=validated_data["phone"],
            profile_pic=validated_data["profile_pic"],
            is_active=True,
        )
        return user


"""class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]
        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                e = "Invalid email or password"
                raise serializers.ValidationError(e, code="unauthorized")
        else:
            e = "Email or password can not be empty"
            raise serializers.ValidationError(e, code="unauthorized")

        refresh = RefreshToken.for_user(user)

        return {
            "token": str(refresh.access_token),
            "refresh": str(refresh)
            # "user": user,
        }
"""


class EditProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "phone", "profile_pic"]
