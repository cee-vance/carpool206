from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Creates and returns a regular user"""
        if not username:
            raise ValueError("Username is required")
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Creates and returns a superuser"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True, primary_key=True)  # Set username as PK
    email = models.EmailField(unique=True, null=True, blank=True)  # Make email optional
    profile_picture = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    social_links = models.JSONField(default=list, blank=True)  # Store social media links as a list
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "username"  # Update the authentication field
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return self.username
