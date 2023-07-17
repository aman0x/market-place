# Create your models here.
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from wholesellerApp.models import Wholeseller
from agentApp.models import Agent
from locationApp.models import *
from masterApp.models import RetailerType
from datetime import datetime
from planApp.models import RetailerPlan
from django.contrib.auth.models import User
from productApp.models import Product
import uuid

RETAILER_STATUS = (
    ("CREATED", "Created"),
    ("PENDING", "Pending Approval"),
    ("KYCAPPROVED", "KYC Approved"),
    ("KYCREJECTED", "KYC Rejected"),
    ("APPROVED", "Approved"),
)

BUSINESS_STATUS = (
    ("NOTREGISTERED", "Not Registered"),
    ("REGISTERED", "Registered")
)

class Retailer(models.Model):
    
    retailer_type = models.ForeignKey(RetailerType, on_delete=models.CASCADE, related_name='retailer_type')
    retailer_business_status = models.CharField(max_length=20, choices=BUSINESS_STATUS, default="REGISTERED")
    retailer_name = models.CharField(max_length=20,null=True,default=None)
    retailer_description = models.TextField(blank=True, null=True)
    retailer_contact_per = models.CharField(max_length=20,null=True,default=None)
    retailer_number = PhoneNumberField(unique=True, blank=True, null=True)
    retailer_wholeseller = models.ManyToManyField(Wholeseller,related_name='retailer_wholeseller',blank=True,null=True)
    retailer_agent = models.ForeignKey(Agent,on_delete=models.CASCADE ,related_name='retailer_agent',blank=True,null=True)
    retailer_altranate_number=PhoneNumberField(blank=True,null=True)
    retailer_plan = models.ForeignKey(RetailerPlan, on_delete=models.CASCADE, related_name="retailer_plan",null=True, blank=True)
    retailer_credit_limit = models.IntegerField(null=True)
    retailer_credit_days = models.IntegerField(null=True)
    retailer_credit_amount = models.IntegerField(null=True)
    retailer_no_of_bills_allowed = models.IntegerField(null=True)
    retailer_opening_balance = models.IntegerField(null=True)
    retailer_state=models.ForeignKey(State,on_delete=models.CASCADE, related_name='retailer_state',null=True, blank=True)
    retailer_district=models.ForeignKey(District,on_delete=models.CASCADE, related_name='retailer_district',null=True, blank=True)
    retailer_city=models.ForeignKey(City,on_delete=models.CASCADE, related_name='retailer_city',null=True, blank=True)
    retailer_status = models.CharField(max_length=20, choices=RETAILER_STATUS, default="CREATED")
    retailer_active=models.BooleanField(default=False)
    retailer_created_at=models.DateTimeField(default=datetime.now, blank=True)
    retailer_otp = models.IntegerField(blank=True, null=True)
    retailer_user = models.ForeignKey(User, related_name="retailer_user", on_delete=models.CASCADE, null=True,blank=True)

    def __str__(self):
        return self.retailer_name
#
class SubCart(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name="cart_product", null=True, blank=True)
    qty = models.IntegerField(null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="retailer", null=True, blank=True)

    def __str__(self):
        return str(self.pk)

class Cart(models.Model):
    cart = models.ManyToManyField(SubCart, related_name="cart", null=True, blank=True)
    order_id = models.CharField(max_length=8, unique=True, editable=False, null=True)

    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_id()
        return super().save(*args, **kwargs)

    def _generate_order_id(self):
        generated_id = str(uuid.uuid4().int)[:8]
        while Cart.objects.filter(order_id=generated_id).exists():
            generated_id = str(uuid.uuid4().int)[:8]
        return generated_id
