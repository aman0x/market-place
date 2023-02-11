from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_description = models.TextField(blank=True)
    category_ref_image = models.ImageField(
        upload_to="photos/%Y/%m/%d", blank=True)
    category_active = models.BooleanField(default=True)
    category_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    category_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    category_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='category_updated_by')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name
