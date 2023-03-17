from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=50, blank=True, default='')
    created_date = models.DateTimeField(default=datetime.now, blank=True)
    updated_date = models.DateTimeField(default=datetime.now, blank=True)
    updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='language_updated_by', default='')



