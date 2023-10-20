from django.db import models
from user.models import User
# Create your models here.

class Prompt(models.Model):
  User = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  gender = models.CharField(max_length=100)
  sensitivity_to_cold = models.CharField(max_length=100)

  def __str__(self):
    return str(self.id)
