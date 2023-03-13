from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class ParentCategory(models.Model):
    parent_category_name = models.CharField(max_length=200)
    parent_category_description = models.TextField(blank=True)
    parent_category_ref_image = models.ImageField(
        upload_to="photos/%Y/%m/%d",  null=True)
    parent_category_active = models.BooleanField(default=True)
    parent_category_added_date = models.DateTimeField(          
        default=datetime.now, blank=True)
    parent_category_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    parent_category_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='parent_category_updated_by')

    class Meta:
        verbose_name_plural = "parentcategories"

    def __str__(self):
        return self.parent_category_name
