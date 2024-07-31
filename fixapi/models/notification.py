# models.py
from django.db import models
from django.conf import settings
from .customer import Customer

class Notification(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    link = models.URLField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.customer} - {self.message[:50]}"

    class Meta:
        ordering = ['-created_at']  # Order notifications by creation time, newest first
