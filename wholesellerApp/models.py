# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from bazaarApp.models import Bazaar
from agentApp.models import Agent
from locationApp.models import *


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
    wholeseller_bazaar = models.ManyToManyField(Bazaar, 'wholeseller')
    wholeseller_type = models.CharField(max_length=11,
                  choices=WHOLESELLER_TYPE,
                  default="INDIVIDUAL"
                )
    wholeseller_agent = models.ManyToManyField(Agent, related_name='agent')
    wholeseller_contact_per = models.ManyToManyField(Agent, related_name='contact_person')
    wholeseller_number = PhoneNumberField(blank=True , null=True)
    wholeseller_city = models.ManyToManyField(City,related_name='wholeseller_city')
    wholeseller_state = models.ManyToManyField(State,related_name='wholeseller_state')
    wholeseller_district = models.ManyToManyField(District,related_name='wholeseller_district')
    wholeseller_image = models.ImageField(upload_to='images/wholeseller/', null=True)
    wholeseller_status = models.CharField(max_length=20, choices= WHOLESELLER_STATUS, default="CREATED")
    is_active = ()
