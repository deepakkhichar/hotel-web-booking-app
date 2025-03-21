from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_hotel = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
