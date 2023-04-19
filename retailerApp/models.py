# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from bazaarApp.models import Bazaar
from agentApp.models import Agent
from locationApp.models import *
from planApp.models import Plan
from agencyApp.models import Agency
from paymentApp.models import Payment
from masterApp.models import RetailerType
from datetime import date


RETAILER_STATUS = (
    ("CREATED", "Created"),
    ("PENDING", "Pending Approval"),
    ("KYCAPPROVED", "KYC Approved"),
    ("KYCREJECTED", "KYC Rejected"),
    ("APPROVED", "Approved"),
)


class Retailer(models.Model):
    retailer_description = models.TextField(blank=True, null=True)
    retailer_name = models.CharField(max_length=200,blank=True)
    retailer_bazaar = models.ManyToManyField(Bazaar, 'retailer_bazaar')
    retailer_plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="retailer_plan", null=True, blank=True)    
    retailer_payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name='payment_detail', null=True, blank=True)
    retailer_type = models.ForeignKey(
        RetailerType, on_delete=models.CASCADE, related_name='retailer_type', null=True, blank=True)
    retailer_firm_name = models.CharField(max_length=20,null=True,default=None)
    retailer_agent = models.ForeignKey(Agent,on_delete=models.CASCADE ,related_name='agent',blank=True,null=True)
    retailer_contact_per = models.CharField(max_length=20,null=True,default=None)
    retailer_number = PhoneNumberField(unique=True, blank=True, null=True)


    retailer_altranate_number=PhoneNumberField(blank=True,null=True)
    retailer_email_id=models.EmailField(max_length=25,null=True)
    retailer_adhar_no=models.CharField(max_length=12,null=True,default=None)
    retailer_gst_no=models.CharField(max_length=15,null=True,default=None)
    retailer_firm_pan_no=models.CharField(max_length=20,null=True,default=None)
    retailer_address=models.CharField(max_length=30,null=True,default=None)
    retailer_landmark=models.CharField(max_length=30,null=True,default=None)
    retailer_city=models.ForeignKey(City,on_delete=models.CASCADE, related_name='retailer_city')
    retailer_state=models.ForeignKey(State,on_delete=models.CASCADE, related_name='retailer_state')
    retailer_district=models.ForeignKey(District,on_delete=models.CASCADE, related_name='retailer_district')
    retailer_pincode_no=models.IntegerField(null=True)
    retailer_adhar_front_image=models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d",null=True)
    retailer_adhar_back_image=models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d",null=True)
    retailer_pan_card_image=models.ImageField(upload_to="pan-image/wholeseller/%y/%m/%d",null=True)
    retailer_image = models.ImageField(
        upload_to='images/wholeseller/', null=True)
    retailer_status = models.CharField(
        max_length=20, choices=retailer_STATUS, default="CREATED")
    retailer_active=models.BooleanField(default=False)
    created_at=models.DateField(auto_now_add=False,default=date.today,blank=True)

    def __str__(self):
        return self.retailer_name
    
