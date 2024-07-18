from django.db import models
from .servicerequest import ServiceRequest
from .category import Category

class ServiceRequestCategory(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name="categories")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="service_requests")