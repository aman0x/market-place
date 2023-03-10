from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from subCategoryApp.models import SubCategory


class Product(models.Model):
    product_subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    product_brand_name=models.CharField(max_length=200)
    product_description = models.TextField(blank=True)
    product_total_weight=models.IntegerField(null=True)
    product_unit=models.IntegerField(null=True)
    product_total_mrp=models.IntegerField(null=True)
    product_per_unit_weight=models.IntegerField(null=True)
    product_mrp=models.IntegerField(null=True)
    product_gst_no=models.IntegerField(null=True)
    product_hsn_code=models.IntegerField(null=True)
    product_upload_front_image = models.ImageField(
        upload_to="photos/%Y/%m/%d", blank=True)
    product_upload_back_image=models.ImageField(upload_to="photos/%Y/%m/%d",blank=True)
    product_upload_mrp_label_image=models.ImageField(upload_to="photos/%Y/%m/%d",blank=True)
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
