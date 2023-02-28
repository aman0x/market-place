from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
#from locality.models import Locality

import os


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "user_{id}/{file}".format(id=instance.pk, file=filename)

class Locality(models.Model):
    locality_name=models.CharField(max_length=50,null=True,default=None)

class Account(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True, related_name='account')
    description = models.TextField(blank=True , null=True)
    user_type = models.CharField(
    max_length=1, choices=settings.USER_TYPE, default=settings.USER_TYPE[0][0])
    locality = models.ForeignKey(
        Locality, on_delete=models.CASCADE, related_name='locality', blank=True , null=True)    
    flat_wing = models.CharField(max_length=200)
    phone = PhoneNumberField(blank=True , null=True)
    device_id = models.TextField(blank=True , null=True)
    profile_image = models.ImageField(
        upload_to=user_directory_path, blank=True, null=True)
    birthdate = models.DateField(
        verbose_name="birth date", blank=True, null=True)
    is_active = ()

    class Meta:
        ordering = ['-user__date_joined']

    def username(self):
        return self.user.username

    def locality_name(self):
        _c = self.locality
        if _c is not None:
            address = _c.name
        else:   
            address = self.flat_wing
        return address

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name    

    def email(self):
        return self.user.email
        
    def __str__(self):
        return self.user.username + '/Date Onboard-' + str(self.user.date_joined)


class Customer(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True, related_name='customer_meta')
    

    def __str__(self):
        return self.account.user.username




class Vendor(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.CASCADE, primary_key=True, related_name='vendor_meta')
    business_name = models.CharField(max_length=200, blank=True, null=True)
    delivery_area_id = models.ForeignKey(Locality, related_name='delivery_area', on_delete=models.CASCADE )
    list_priority = models.IntegerField(blank=True, null=True)
    vendor_type = models.CharField(
        max_length=2, choices=settings.VENDOR_TYPE, default=settings.VENDOR_TYPE[0][0])
    deliver_time = models.CharField(max_length=10, blank=True, null=True)
    aadhaar_number = models.IntegerField(blank=True, null=True)
    doc_image = models.ImageField(
        upload_to=user_directory_path, blank=True)
    # vendor new field
    serviceable_area = models.IntegerField(blank=True, null=True)
    delivery_charges = models.IntegerField(blank=True, null=True)
    delivery_charges_limit = models.IntegerField(blank=True, null=True)
    packaging_charges = models.IntegerField(blank=True, null=True)
    packaging_charges_limit = models.IntegerField(blank=True, null=True)
    min_order_value = models.IntegerField(blank=True, null=True)
    business_hours = models.IntegerField(blank=True, null=True)
    vendor_status = models.BooleanField(default=True, blank=True, null=True)
    is_disabled = models.BooleanField(default=False, blank=True, null=True)
    unique_url = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.account.user.username

    def delivery_area_name(self):
        _c = self.delivery_area_id
        if _c is not None:
            address = _c.area
        else:   
            address = self.building_name
        return address


PAYMENT_CHOICE=(
    ("CASH","Cash"),
    ("CREDIT","Credit"),
)
class UserPayment(models.Model):
    payment_choice=models.CharField(max_length=50,choices=PAYMENT_CHOICE,default="Cash")
    payment_user = models.ForeignKey(Account, related_name='payment_account', on_delete=models.CASCADE )
    payment_ref = models.ImageField(
        upload_to=user_directory_path, blank=True)
    payment_option = models.CharField(
        max_length=2, choices=settings.PAYMENT_OPTION, default=settings.PAYMENT_OPTION[0][0])
    payment_user_key = models.CharField(max_length=20)
    
    def __str__(self):
        return self.payment_user.user.username
