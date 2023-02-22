from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from subCategoryApp.models import SubCategory


class Product(models.Model):
    product_subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_description = models.TextField(blank=True)
    product_ref_image = models.ImageField(
        upload_to="photos/%Y/%m/%d", blank=True)
    product_active = models.BooleanField(default=True)
    product_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    product_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    product_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product_updated_by')

    class Meta:
        verbose_name_plural = "products"

    def __str__(self):
        return self.product_name
