from django.conf import settings
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from bazaarApp.models import Bazaar


class ParentCategory(models.Model):
    parent_category_name = models.CharField(max_length=200, unique=True)
    parent_category_description = models.TextField(blank=True)
    parent_category_ref_image = models.ImageField(
        upload_to="image/parentcategory/%Y/%m/%d",  null=True)
    bazaar = models.ForeignKey(
        Bazaar, on_delete=models.CASCADE, related_name='parent_category_bazaar')
    parent_category_added_date = models.DateTimeField(          
        default=datetime.now, blank=True)
    parent_category_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    parent_category_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='parent_category_updated_by')
    parent_category_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "parentcategories"
    
    def __str__(self):
        return self.parent_category_name