# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from bazaarApp.models import Bazaar
from agentApp.models import Agent
from locationApp.models import *
from planApp.models import Plan
from agencyApp.models import Agency
from paymentApp.models import Payment
from parentCategoryApp.models import ParentCategory
from categoryApp.models import Category
from productApp.models import Product
from datetime import date
import jsonfield
from django.db import IntegrityError


WHOLESELLER_TYPE = (
    ("INDIVIDUAL", "Individual"),
    ("WHOLESELLER", "Wholeseller"),
    ("SEMIWHOLESELLER","SemiWholeseller")
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
    wholeseller_name = models.CharField(max_length=200,blank=True)
    wholeseller_bazaar = models.ManyToManyField(Bazaar, 'wholeseller')
    wholeseller_plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="chooseplan", null=True, blank=True)
    wholeseller_payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name='payment_detail', null=True, blank=True)
    wholeseller_type = models.CharField(max_length=15,
                                        choices=WHOLESELLER_TYPE,
                                        default="INDIVIDUAL"
                                        )
    wholeseller_firm_name = models.CharField(max_length=20,null=True,default=None)
    wholeseller_agent = models.ForeignKey(Agent,on_delete=models.CASCADE ,related_name='agent',blank=True,null=True)
    wholeseller_contact_per = models.CharField(max_length=20,null=True,default=None)
    wholeseller_number = PhoneNumberField(unique=True, blank=True, null=True)
    wholeseller_altranate_number=PhoneNumberField(blank=True,null=True)
    wholeseller_email_id=models.EmailField(max_length=25,null=True)
    wholeseller_adhar_no=models.CharField(max_length=12,null=True,default=None)
    wholeseller_gst_no=models.CharField(max_length=15,null=True,default=None)
    wholeseller_firm_pan_no=models.CharField(max_length=20,null=True,default=None)
    wholeseller_address=models.CharField(max_length=30,null=True,default=None)
    wholeseller_landmark=models.CharField(max_length=30,null=True,default=None)
    wholeseller_city=models.ForeignKey(City,on_delete=models.CASCADE, related_name='wholeseller_city')
    wholeseller_state=models.ForeignKey(State,on_delete=models.CASCADE, related_name='wholeseller_state')
    wholeseller_district=models.ForeignKey(District,on_delete=models.CASCADE, related_name='wholeseller_district')
    wholeseller_pincode_no=models.IntegerField(null=True)
    wholeseller_adhar_front_image=models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d",null=True)
    wholeseller_adhar_back_image=models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d",null=True)
    wholeseller_pan_card_image=models.ImageField(upload_to="pan-image/wholeseller/%y/%m/%d",null=True)
    wholeseller_image = models.ImageField(
        upload_to='images/wholeseller/', null=True)
    wholeseller_status = models.CharField(
        max_length=20, choices=WHOLESELLER_STATUS, default="CREATED")
    wholeseller_otp = models.IntegerField(blank=True, null=True)
    wholeseller_user = models.ForeignKey(
        User, related_name="wholeseller_user", on_delete=models.CASCADE, null=True, blank=True)
    wholeseller_active=models.BooleanField(default=False)
    get_wholeseller_location_json_data = jsonfield.JSONField(default={}, null=True,)

    created_at=models.DateField(auto_now_add=False,default=date.today,blank=True)

    def __str__(self):
        return self.wholeseller_name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            # If the Wholeseller object is being created for the first time
            try:
                user = User.objects.create_user(
                    username=self.wholeseller_number, password='Test@!Test123')
                self.wholeseller_user = user
            except IntegrityError:
                # If a user with the same username already exists, retrieve the existing user and update its fields
                user = User.objects.get(username=self.wholeseller_number)
                user.set_password('Test@!Test123')
                user.save()
                self.wholeseller_user = user
        super().save(*args, **kwargs)

class Branch(models.Model):
    branch_name= models.CharField(max_length=200,null=False)
    manager_name= models.CharField(max_length=200,null=True)
    branch_phone= PhoneNumberField(blank=True, null=True)
    category_name = models.ForeignKey(ParentCategory, on_delete=models.CASCADE, related_name='branch_category')
    item_name = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='branch_item')
    subcategory_name= models.ForeignKey(Category, on_delete=models.CASCADE, related_name='branch_subcategory')
    address_line1 = models.CharField(max_length=300, null=True)
    address_line2 = models.CharField(max_length=300, null=True)
    landmark = models.CharField(max_length=300, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='branch_city')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='branch_state')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='branch_district')
    pincode_no = models.IntegerField(null=True)
    created_at = models.DateField(auto_now_add=False, default=date.today, blank=True)
    branch_wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE,related_name='branch_wholeseller')

    def __str__(self):
        if self.branch_name != None:
            return self.branch_name