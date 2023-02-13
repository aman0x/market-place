# Create your models here.
from django.db import models
from bazaarApp.models import Bazaar
from phonenumber_field.modelfields import PhoneNumberField


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

class Agent(models.Model):
    
    agent_bazaar = models.ManyToManyField(Bazaar, related_name="agent")
    agent_description = models.TextField(blank=True, null=True)
    agent_name = models.CharField(max_length=200)
    agent_type = models.CharField(max_length=11,
                  choices=AGENT_TYPE,
                  default="INDIVIDUAL"
                )
    agent_number = PhoneNumberField(blank=True , null=True)
    agent_state = models.CharField(max_length=200, null=True)
    agent_district = models.CharField(max_length=200, null=True)
    agent_city = models.CharField(max_length=200, null=True)
    agent_image = models.ImageField(upload_to='images/agent/', null=True)
    agent_status = models.CharField(max_length=20, choices= AGENT_STATUS, default="CREATED")
    is_active = ()




