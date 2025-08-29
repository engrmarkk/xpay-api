from apis.users.models import User, UserSession
from rest_framework import serializers
from api_services.utils import validate_password, validate_email
from django.contrib.auth import authenticate
from datetime import datetime, timedelta


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    id = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        return user


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        email_valid = validate_email(email)
        if email_valid:
            raise serializers.ValidationError(email_valid)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        password_res = validate_password(password)
        if password_res:
            raise serializers.ValidationError(password_res)
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

"""
class UserSessionSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    otp = serializers.CharField(max_length=6, required=False)
    otp_expiry = serializers.DateTimeField(read_only=True)
    reset_p = serializers.CharField(max_length=100, required=False)
    reset_p_expiry = serializers.DateTimeField(read_only=True)
    reset_p_broken = serializers.BooleanField(default=False)

    def validate(self, data):
        user = self.context["user"]
        if not user:
            raise serializers.ValidationError("User not found")
        return data

    def create(self, validated_data):
        user = self.context["user"]
        existing_session = UserSession.objects.filter(user=user).first()
        if existing_session:
            existing_session.delete()
        return UserSession.objects.create(user=user, **validated_data)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # email = data.get("email")
        user = self.context["user"]
        if not user:
            raise serializers.ValidationError("User not found")
        return data

    def create(self, validated_data):
        user = self.context["user"]
        expiry = datetime.now() + timedelta(minutes=10)
        reset_p = f"ly{generate_random_string()}"
        usersession = UserSession.objects.filter(user=user).first()
        if usersession:
            usersession.reset_p = reset_p
            usersession.reset_p_expiry = expiry
            usersession.reset_broken = False
            usersession.save()
        else:
            usersession = UserSession(user=user, reset_p=reset_p, reset_p_expiry=expiry)
            usersession.save()
        return usersession


class ResetPasswordVerifySerializer(serializers.Serializer):
    reset_p = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()

    def validate(self, data):
        reset_p = data.get("reset_p")
        new_password = data.get("new_password")
        confirm_password = data.get("confirm_password")
        if not reset_p:
            raise serializers.ValidationError("Pls provide reset password link")

        if not new_password:
            raise serializers.ValidationError("Pls provide new password")

        if not confirm_password:
            raise serializers.ValidationError("Pls provide confirm password")

        usersession = UserSession.objects.filter(reset_p=reset_p).first()
        if not usersession:
            raise serializers.ValidationError("Session not found")
        if usersession.reset_p_expiry < datetime.now():
            raise serializers.ValidationError("Session expired")
        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        reset_p = validated_data["reset_p"]
        new_password = validated_data["new_password"]
        usersession = UserSession.objects.filter(reset_p=reset_p).first()
        user = usersession.user
        user.set_password(new_password)
        user.save()
        usersession.delete()
        return user
"""