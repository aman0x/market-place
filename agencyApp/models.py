from django.db import models
from locationApp.models import *

class Agency(models.Model):
    firm_name=models.CharField(max_length=100,default=None,blank=True)
    gst_number=models.CharField(max_length=15,default=None, blank=True, null=True)
    pan_number=models.CharField(max_length=20,default=None,blank=True)
    address=models.CharField(max_length=50,default=None,blank=True)
    landmark=models.CharField(max_length=50,default=None,blank=True)
    state=models.ManyToManyField(State,related_name="agency_state")
    district=models.ManyToManyField(District,related_name="agency_district")
    city=models.ManyToManyField(City,related_name="agency_city")
    pin_code=models.CharField(max_length=20,default=None,blank=True)
    gst_image=models.ImageField(upload_to="image/agency/",null=True)
    pancard_image=models.ImageField(upload_to='image/agent/',null=True)
