from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, null=False, default="")
    phone_number = models.CharField(max_length=10, null=True)
    alt_phone_number = models.CharField(max_length=10, null=True)
    address = models.TextField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=50, null=True)
    pincode = models.CharField(max_length=50, null=True)
    # latitude = models.FloatField()
    # longitude = models.FloatField()
