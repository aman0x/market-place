# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from parentCategoryApp.models import ParentCategory
from datetime import datetime
from categoryApp.models import Category
from subCategoryApp.models import SubCategory
from productApp.models import Product



class Bazaar(models.Model):
    bazaar_description = models.TextField(blank=True, null=True)
    bazaar_name = models.CharField(max_length=200, null=True)
    bazaar_state = models.CharField(max_length=200, null=True)
    bazaar_district = models.CharField(max_length=200, null=True)
    bazaar_city = models.CharField(max_length=200, null=True)
    bazaar_image = models.ImageField(upload_to='images/', null=True)
    bazaar_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bazaar_updated_by')

    is_active = ()

    def username(self):
        return self.user.username


class BazaarData(models.Model):
    bazaar_gorup_category = models.ManyToManyField(ParentCategory)
    bazaar_category = models.ManyToManyField(Category)
    bazaar_subcategory = models.ManyToManyField(SubCategory)
    bazaar_product = models.ManyToManyField(Product)



