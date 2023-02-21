from django.db import models


class Agency(models.Model):
    Firm_name=models.CharField(max_length=100,default=None,blank=True)
    Gst_Number=models.IntegerField()
    Pan_Number=models.CharField(max_length=20,default=None,blank=True)
    Address=models.CharField(max_length=50,default=None,blank=True)
    Landmark=models.CharField(max_length=50,default=None,blank=True)
    State=models.CharField(max_length=50,default=None,blank=True)
    City=models.CharField(max_length=50,default=None,blank=True)
    Pin_code=models.CharField(max_length=20,default=None,blank=True)
    Gst_image=models.ImageField(upload_to="image/agency/",null=True)
    PanCard_image=models.ImageField(upload_to='image/agent/',null=True)
