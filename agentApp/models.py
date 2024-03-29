# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from bazaarApp.models import Bazaar
from phonenumber_field.modelfields import PhoneNumberField
from agencyApp.models import Agency
from locationApp.models import *
from django.db import IntegrityError
import random
import string
import jsonfield


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

AGENT_COMMISSION_TYPE = (
    ("PERCUSTOMER", "Percustomer"),
    ("PERPLAN", "Perplan")
)

AGENT_COMMISSION_VALUE_TYPE = (
    ("PERCENTAGE", "Percentage"),
    ("AMOUNT", "Amount")
)

AGENT_GENDER = (
    ("MALE", "Male"),
    ("FEMALE", "Female")
)

class Agent(models.Model):

    agent_bazaar = models.ManyToManyField(Bazaar, related_name="agent")
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, related_name="agent_agency")
    agent_description = models.TextField(blank=True, null=True)
    agent_name = models.CharField(max_length=200)
    agent_type = models.CharField(max_length=11, choices=AGENT_TYPE,default="INDIVIDUAL")
    agent_number = PhoneNumberField(unique=True,blank=True, null=True)
    agent_altranate_mobile_number = PhoneNumberField(blank=True, null=True)
    agent_email = models.EmailField(null=True)
    agent_gender = models.CharField(max_length=10, choices=AGENT_GENDER, default="MALE")
    agent_date_of_birth = models.DateField(auto_now_add=False, null=True)
    agent_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    agent_landmark = models.CharField(max_length=100, default=None, blank=True, null=True)
    agent_state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, related_name="agent_state")
    agent_city = models.ForeignKey(City,  on_delete=models.CASCADE, null=True, related_name="agent_city")
    agent_district = models.ForeignKey(District,  on_delete=models.CASCADE, null=True, related_name="agent_district")
    agent_assigned_state = models.ManyToManyField(State, related_name="agent_assigned_state")
    agent_assigned_city = models.ManyToManyField(City, related_name="agent_assigned_city")
    agent_assigned_district = models.ManyToManyField(District, related_name="agent_assigned_district")
    agent_pincode = models.IntegerField(null=True)
    agent_commission_type = models.CharField(max_length=20, choices=AGENT_COMMISSION_TYPE, default="PERCUSTOMER")
    agent_commission_value_type =models.CharField(max_length=20, choices=AGENT_COMMISSION_VALUE_TYPE, default="AMOUNT")
    agent_commission_value =models.CharField(max_length=10, default=None, blank=True, null=True)
    agent_adharcard_no = models.CharField(max_length=12, default=None, blank=True, null=True)
    agent_adhar_front_image = models.ImageField(upload_to="image/agent/", null=True)
    agent_adhar_back_image = models.ImageField(upload_to="image/agent/", default=None, null=True)
    agent_pancard_image = models.ImageField(upload_to="image/agent/", default=None, null=True)
    agent_pancard_no = models.CharField(max_length=50, default=None, blank=True, null=True)
    agent_image = models.ImageField(upload_to='images/agent/', null=True)
    agent_status = models.CharField(max_length=20, choices=AGENT_STATUS, default="CREATED")
    agent_otp = models.IntegerField(blank=True, null=True)
    agent_user = models.ForeignKey(User, related_name="agent_user", on_delete=models.CASCADE, null=True, blank=True)
    is_active = ()
    agent_active = models.BooleanField(default=False)
    get_agent_location_json_data = jsonfield.JSONField(default={}, null=True,)
    #agent_date_of_creation = models.DateTimeField(auto_now_add=False,null=True,blank=True)


    def __str__(self):
        return self.agent_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the Agent object is being created for the first time
            try:
                user = User.objects.create_user(
                    username=self.agent_number, password='Test@!Test123')
                self.agent_user = user
            except IntegrityError:
                # If a user with the same username already exists, retrieve the existing user and update its fields
                user = User.objects.get(username=self.agent_number)
                user.set_password('Test@!Test123')
                user.save()
                self.agent_user = user
        super().save(*args, **kwargs)


PLAN_CHOICE = (
    ("FREEPLAN", "FreePlan"),
    ("PLANPAID", "PlanPaid"),
)


class AgentCommisionRedeem(models.Model):
    plan = models.CharField(
        max_length=15, choices=PLAN_CHOICE, default="PLANPAID")
    minimum_no_of_invoice_genrated = models.IntegerField(null=True)
    amount_reimbursed_on_particular_days_percent = models.IntegerField(
        null=True)
    no_of_days_between_redemption = models.IntegerField(null=True)

    def __str__(self):
        return self.plan
