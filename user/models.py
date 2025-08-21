import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin


class AppUserManager(BaseUserManager):
    def create_user(self, email, phone_number, username, password=None):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)   # ✅ Save user to DB
        return user

    def create_superuser(self, email, username, password=None, phone_number=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            phone_number=phone_number
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    phone_number = models.CharField(max_length=14, unique=True, null=True, blank=True)  # ✅ allow null for superusers
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_rider = models.BooleanField(default=False)

    # Rider location
    latitude = models.CharField(max_length=60, null=True, blank=True)
    longitude = models.CharField(max_length=60, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AppUserManager()

    class Meta:
        ordering = ['-created_at', '-updated_at']  # ✅ newest first

    def save(self, *args, **kwargs):
        if self.id:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
