from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    tutor=models.CharField(max_length=30)
    dinero=models.IntegerField()

    REQUIRED_FIELDS= ['tutor', 'dinero']