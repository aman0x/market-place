from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from locationApp.models import *
from masterApp.models import RetailerType
    
class Bazaar(models.Model):
    bazaar_name = models.CharField(max_length=200, null=True)
    bazaar_description = models.TextField(blank=True, null=True)
    bazaar_image = models.ImageField(
        upload_to='image/bazaar/%Y/%m/%d')
    bazaar_state = models.ManyToManyField(
        State, related_name='bazaar_state')
    bazaar_district = models.ManyToManyField(
        District, related_name='bazaar_district')
    bazaar_city = models.ManyToManyField(
        City, related_name='bazaar_city')
    bazaar_added_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_date = models.DateTimeField(
        default=datetime.now, blank=True)
    bazaar_updated_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bazaar_updated_by', null=True)
    bazaar_steps = models.IntegerField(null=True, default=None)
    bazaar_retailer_type = models.ManyToManyField(
        RetailerType, related_name="bazaar_retailer_type", blank=True)
    bazaar_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "bazaars"
    
    def get_values(self):
        return [self.bazaar_state, self.bazaar_district]

    def __str__(self):
        if self.bazaar_name==None:
            return "Null"
        return self.bazaar_name




