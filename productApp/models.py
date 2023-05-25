from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from subCategoryApp.models import SubCategory,Category,ParentCategory,Bazaar
import hashlib
from masterApp.models import Unit

class Product(models.Model):
    product_name = models.CharField(max_length=200)    
    product_description = models.TextField(blank=True)
    product_brand_name=models.CharField(max_length=200)
    product_upload_front_image = models.ImageField(
        upload_to="image/product/%Y/%m/%d", null=True)
    product_upload_back_image=models.ImageField(
        upload_to="image/product/%Y/%m/%d",null=True)
    product_upload_mrp_label_image=models.ImageField(
        upload_to="image/product/%Y/%m/%d",null=True)
    product_total_weight=models.IntegerField(null=True)
    product_unit=models.IntegerField(null=True)
    product_total_mrp=models.IntegerField(null=True)
    product_per_unit_weight=models.IntegerField(null=True)
    product_mrp=models.IntegerField(null=True)
    product_base_price = models.IntegerField(null=True)
    product_gst_no=models.CharField(max_length=15,default=None, blank=True, null=True)
    product_hsn_code=models.IntegerField(null=True)
    bazaar = models.ForeignKey(
        Bazaar, on_delete=models.CASCADE, related_name='product_bazaar')
    category_group = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, related_name='product_parent_category')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='product_category')
    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name='product_subcategory')
    product_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    product_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    product_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='product_updated_by')
    product_barcode_number = models.CharField(max_length=12, blank=True)
    product_stocks = models.IntegerField(null=True)
    product_min_quantity = models.IntegerField(null=True)
    product_max_quantity = models.IntegerField(null=True)
    product_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "products"
        
    def save(self, *args, **kwargs):
        if not self.product_barcode_number:  # Generate barcode only if it's not already set
            self.product_barcode_number = self.generate_barcode()
        super(Product, self).save(*args, **kwargs)

    def generate_barcode(self):
        data = self.product_name + self.product_brand_name
        sha256 = hashlib.sha256()
        sha256.update(data.encode('utf-8'))
        hash_value = sha256.hexdigest()
        barcode = str(int(hash_value, 16))[:12]

        return barcode.zfill(12)

    def __str__(self):
        return self.product_name
