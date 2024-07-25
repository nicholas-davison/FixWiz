from django.db import models
from .customer import Customer
from .contractor import Contractor
from .category import Category

class ServiceRequest(models.Model):
    URGENCY_CHOICES = [
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    title = models.CharField(max_length=25)
    date_created = models.DateField(auto_now_add=True)
    urgency_level = models.CharField(max_length=10, choices=URGENCY_CHOICES, default='medium')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL, null=True, blank=True)
    date_claimed = models.DateField(null=True, blank=True)
    date_completed = models.DateField(null=True, blank=True)

    request_categories = models.ManyToManyField(Category, through='ServiceRequestCategory')

    def get_categories(self):
        return self.request_categories.all()
    
    def get_status(self):
        if not self.contractor:
            return 'open'
        elif not self.date_completed:
            return 'in progress'
        else:
            return 'closed'