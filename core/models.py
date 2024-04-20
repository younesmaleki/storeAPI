from datetime import timezone
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f'{self.username}'