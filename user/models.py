from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # full_name = models.CharField(max_length=255)
    # address = models.CharField(max_length=255)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']