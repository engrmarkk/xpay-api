from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from api_services.utils import hex_uuid



class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and return a superuser with the given email and password."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    id = models.CharField(
        primary_key=True, max_length=32, default=hex_uuid, editable=False
    )
    # i dont need username column
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    device_id = models.CharField(max_length=100)
    password = models.TextField()
    address = models.TextField()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class UserSession(models.Model):
    id = models.CharField(
        primary_key=True, max_length=32, default=hex_uuid, editable=False
    )
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField()
    reset_p = models.CharField(max_length=100)
    reset_p_expiry = models.DateTimeField()
    reset_p_broken = models.BooleanField(default=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.otp