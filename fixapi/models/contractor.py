from django.db import models
from django.contrib.auth.models import User

class Contractor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.IntegerField()
    address = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=True)