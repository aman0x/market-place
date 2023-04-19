from django.db import models

UNIT_TYPE = (
    ("QUANTITY", "Quantity"),
    ("WEIGHT", "Weight"),
)


class Unit(models.Model):
    unit_type = models.CharField(
        max_length=15, choices=UNIT_TYPE, default="QUANTITY", unique=True)
    unit_name=models.CharField(max_length=30,default=None)

    def __str__(self):
        return self.unit_name
    
class WholesellerType(models.Model):
    wholeseller_type_image = models.ImageField(
        upload_to="image/master/", null=True)
    wholeseller_type_name = models.CharField(
        max_length=30, null=True, default=None, unique=True)
    
    def __str__(self):
        return self.wholeseller_type_name


class RetailerType(models.Model):
    retailer_type_image = models.ImageField(
        upload_to="image/master/", null=True)
    retailer_type_name = models.CharField(
        max_length=30, null=True, default=None, unique=True)
    
    def __str__(self):
        return self.retailer_type_name
