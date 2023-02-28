# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from parentCategoryApp.models import ParentCategory
from datetime import datetime
from categoryApp.models import Category
from subCategoryApp.models import SubCategory
from productApp.models import Product
from locationApp.models import *


class Bazaar(models.Model):
    bazaar_description = models.TextField(blank=True, null=True)
    bazaar_name = models.CharField(max_length=200, null=True)
    bazaar_state = models.ManyToManyField(
        State, related_name='bazaar_state')
    bazaar_city = models.ManyToManyField(
        City, related_name='bazaar_city')
    bazaar_district = models.ManyToManyField(
        District, related_name='bazaar_district')
    bazaar_image = models.ImageField(upload_to='images/', null=True)
    bazaar_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bazaar_updated_by')
    bazaar_gorup_category = models.ManyToManyField(ParentCategory, related_name='bazaar_group_category')
    bazaar_category = models.ManyToManyField(
        Category, related_name='bazaar_category')
    bazaar_subcategory = models.ManyToManyField(
        SubCategory, related_name='bazaar_subcategory')
    bazaar_product = models.ManyToManyField(
        Product, related_name='bazaar_product')
    is_active = ()

    def username(self):
        return self.user.username





