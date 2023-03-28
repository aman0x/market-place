from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from parentCategoryApp.models import ParentCategory,Bazaar



class Category(models.Model):
    category_name = models.CharField(max_length=200)
    category_description = models.TextField(blank=True)
    category_ref_image = models.ImageField(
        upload_to="image/category/%Y/%m/%d",  null=True)
    bazaar = models.ForeignKey(
        Bazaar, on_delete=models.CASCADE, related_name='category_bazaar')
    category_group = models.ForeignKey(
        ParentCategory, on_delete=models.CASCADE, related_name='category_parent_category')
    category_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    category_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    category_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='category_updated_by')
    category_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.category_name