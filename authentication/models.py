from typing import Any, Coroutine
from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractUser
# Create your models here.
class SiteSettings(models.Model):
    email = models.EmailField(max_length=254, help_text="The email address for the site.")
    phone = models.CharField(max_length=20, help_text="The phone number for the site.")
    facebook_url = models.URLField(max_length=200, help_text="The Facebook URL for the site.")
    terms_and_conditions = models.TextField(help_text="The terms and conditions for the site.")
    privacy_policy = models.TextField(help_text="The privacy policy for the site.")


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)
 
class User(AbstractUser):
      username = None
      first_name = models.CharField(max_length = 255)
      last_name = models.CharField(max_length=255)
      email = models.CharField(max_length = 255,unique = True)
      password = models.CharField(max_length = 255) 
      gender = models.CharField(max_length=255,default="")
      city = models.CharField(max_length=255,default="")
      birth_date = models.DateField(null= True,blank=True)
      picture = models.ImageField(null = True,blank=True)
      objects = CustomUserManager()
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = []
      
      def __str__(self) -> str:
          return f"{self.first_name} {self.last_name}"
      