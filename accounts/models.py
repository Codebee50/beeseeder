from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

import uuid
import pytz
from django.utils.translation import gettext_lazy as _
from .managers import CustomUserManager


# Create your models here.


class Country(models.Model):
    code = models.CharField(max_length=3, unique=True)
    currency = models.CharField(max_length=3)
    flag = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return f"{self.name} - {self.code}"

class UserAccount(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(max_length=100)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False) 
    is_superuser=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_photo = models.ImageField(upload_to='profile-images/', null=True, blank=True)
    country_iso = models.CharField(max_length=3, null=True, blank=False)
    timezone = models.CharField(max_length=50, choices=[(tz, tz) for tz in pytz.all_timezones], default="UTC")
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    bio = models.TextField(null=True, blank=True)
    
    
    REQUIRED_FIELDS = ['username']
    USERNAME_FIELD = 'email'
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("UserAccount")
        ordering = ("-created_at",)
        permissions = []

    def __str__(self):
        return f"{self.email}"