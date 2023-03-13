from django.db import models
from datetime import datetime
from django.conf import settings
from categoryApp.models import Category,ParentCategory
from django.contrib.auth.models import User


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=200)
    subcategory_description = models.TextField(blank=True)
    subcategory_ref_image = models.ImageField(
        upload_to="photos/%Y/%m/%d", null=True)
    subcategory_active = models.BooleanField(default=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategory')
    category_group = models.ForeignKey(ParentCategory, on_delete=models.CASCADE)
    subcategory_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    subcategory_updated_date = models.DateTimeField(default=datetime.now, blank=True)
    subcategory_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='subcategory_updated_by')

    class Meta:
        verbose_name_plural = "subcategories"

    def __str__(self):
        return self.subcategory_name

