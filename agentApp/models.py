# Create your models here.
from django.db import models
from bazaarApp.models import Bazaar
from phonenumber_field.modelfields import PhoneNumberField
from categoryApp.models import Category


AGENT_TYPE = (
    ("INDIVIDUAL", "Individual"),
    ("AGENCY", "Agency"),
    ("SALESMAN", "Salesman"),
)

AGENT_STATUS = (
    ("CREATED", "Created"),
    ("PENDING", "Pending Approval"),
    ("KYCAPPROVED", "KYC Approved"),
    ("KYCREJECTED", "KYC Rejected"),
    ("APPROVED", "Approved"),
)

AGENT_COMMISION = (
    ("PERCUSTOMER", "Percustomer"),
    ("PERPLAN", "Perplan")
)

AGENT_GENDER=(
    ("MALE","Male"),
    ("FEMALE","Female")
)
class Agent(models.Model):
    
    agent_bazaar = models.ManyToManyField(Bazaar, related_name="agent")
    agent_description = models.TextField(blank=True, null=True)
    agent_name = models.CharField(max_length=200)
    agent_type = models.CharField(max_length=11,
                  choices=AGENT_TYPE,
                  default="INDIVIDUAL"
                )
    agent_number = PhoneNumberField(blank=True , null=True)
    agent_altranate_mobile_number=PhoneNumberField(blank=True,null=True)
    agent_email = models.EmailField(null=True)
    agent_gender=models.CharField(max_length=10,choices=AGENT_GENDER,default="Male")
    agent_date_of_birth = models.DateTimeField(auto_now_add=False, null=True)
    agent_address=models.CharField(max_length=100,default=None, blank=True, null=True)
    agent_landmark=models.CharField(max_length=100,default=None,blank=True, null=True)
    agent_state = models.CharField(max_length=200, null=True)
    agent_district = models.CharField(max_length=200, null=True)
    agent_city = models.CharField(max_length=200, null=True)
    agent_pincode=models.IntegerField(null=True)
    agent_commision = models.ForeignKey(
        "ManageCommision", on_delete=models.CASCADE, null=True)
    agent_adharcard_no = models.IntegerField(null=True)
    agent_adhar_front_image=models.ImageField(upload_to="image/agent/",null=True)
    agent_adhar_back_image=models.ImageField(upload_to="image/agent/",default=None ,null=True)
    agent_pancard_image=models.ImageField(upload_to="image/agent/",default=None, null=True)
    agent_pancard_no = models.CharField(max_length=50, default=None, blank=True, null=True)
    agent_image = models.ImageField(upload_to='images/agent/', null=True)
    agent_status = models.CharField(max_length=20, choices= AGENT_STATUS, default="CREATED")
    is_active = ()



class ManageCommision(models.Model):
    
    agent_manage_commision = models.CharField(
        max_length=15, choices=AGENT_COMMISION, default="PERPLAN")
    agent_commision_value = models.IntegerField(blank=True, null=True)

