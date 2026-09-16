from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=100)
    website = models.URLField()
    api_url = models.URLField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
