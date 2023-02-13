# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from bazaarApp.models import Bazaar
from agentApp.models import Agent


WHOLESELLER_TYPE = (
    ("INDIVIDUAL", "Individual"),
    ("WHOLESELLER", "Wholeseller"),
)

WHOLESELLER_STATUS = (
    ("CREATED", "Created"),
    ("PENDING", "Pending Approval"),
    ("KYCAPPROVED", "KYC Approved"),
    ("KYCREJECTED", "KYC Rejected"),
    ("APPROVED", "Approved"),
)

class Wholeseller(models.Model):
    wholeseller_description = models.TextField(blank=True, null=True)
    wholeseller_name = models.CharField(max_length=200)
    wholeseller_bazaar = models.ManyToManyField(Bazaar)
    wholeseller_type = models.CharField(max_length=11,
                  choices=WHOLESELLER_TYPE,
                  default="INDIVIDUAL"
                )
    wholeseller_agent = models.ManyToManyField(Agent, related_name='w_agent')
    wholeseller_contact_per = models.ManyToManyField(Agent, related_name='w_contact_person')
    wholeseller_number = PhoneNumberField(blank=True , null=True)
    wholeseller_state = models.CharField(max_length=200, null=True)
    wholeseller_district = models.CharField(max_length=200, null=True)
    wholeseller_city = models.CharField(max_length=200, null=True)
    wholeseller_image = models.ImageField(upload_to='images/wholeseller/', null=True)
    wholeseller_status = models.CharField(max_length=20, choices= WHOLESELLER_STATUS, default="CREATED")
    is_active = ()
