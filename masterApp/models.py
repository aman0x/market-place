from django.db import models
from bazaarApp.models import Bazaar

UNIT_TYPE = (
    ("QUANTITY", "Quantity"),
    ("WEIGHT", "Weight"),
)


class Unit(models.Model):
    unit_type = models.CharField(
        max_length=15, choices=UNIT_TYPE, default="QUANTITY")
    unit_name=models.CharField(max_length=30,default=None, unique=True)

    def __str__(self):
        return self.unit_name
    
class WholesellerType(models.Model):
    # wholeseller_type_image = models.ImageField(upload_to="image/master/", null=True)
    wholeseller_type_name = models.CharField(max_length=30, null=True, default=None, unique=True)
    bazaar = models.ForeignKey(Bazaar, on_delete=models.CASCADE, related_name="wholeseller_bazaar", null=True, blank=True)
    def __str__(self):
        return self.wholeseller_type_name


class RetailerType(models.Model):
    # retailer_type_image = models.ImageField(upload_to="image/master/", null=True)
    retailer_type_name = models.CharField(max_length=30, null=True, default=None, unique=True)
    bazaar = models.ForeignKey(Bazaar,on_delete=models.CASCADE, related_name="retailer_bazaar", null=True, blank=True)
    
    def __str__(self):
        return self.retailer_type_name

class Colour(models.Model):
    colour=models.CharField(max_length=30,default=None, unique=True)
    colour_description = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return self.colour
    
class Size(models.Model):
    size=models.CharField(max_length=30,default=None, unique=True)
    size_description = models.CharField(max_length=100, default=None, null=True)

    def __str__(self):
        return self.size