from django.db import models
from .customer import Customer
from .contractor import Contractor

class ServiceRequest(models.Model):
    URGENCY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    date_created = models.DateField(auto_now_add=True)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True, blank=True)
    date_claimed = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)