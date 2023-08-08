# Create your models here.
import datetime

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
import jsonfield

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

RETAILER_NOTIFICATION_STATUS = (
    ("NEW", "New Request"),
    ("OLD", "Old Request"),
    ("ACCEPT", "Accepted Request"),
    ("REJECT", "Rejected Request"),
    ("SAVE", "Save For Later")
)

class RetailerMobile(models.Model):
    retailer_number = PhoneNumberField(blank=True, null=True)
    retailer_otp = models.IntegerField(blank=True, null=True)
    retailer_user = models.ForeignKey(User, related_name="retailer_user", on_delete=models.CASCADE, null=True,blank=True)
    is_auto_fill = models.BooleanField(null=True)
    def __str__(self):
        return str(self.retailer_number)


RETAILER_PLAN= (
    ('CASH', 'Cash'),
    ('PLATINUM', 'Platinum'),
    ('DIAMOND', 'Diamond'),
    ('GOLD', 'Gold'),
    ('BRONZE', 'Bronze')
)

class Retailer(models.Model):
    
    retailer_type = models.ForeignKey(RetailerType, on_delete=models.CASCADE, related_name='retailer_type',null=True,default=None)
    retailer_business_status = models.CharField(max_length=20, choices=BUSINESS_STATUS, default="REGISTERED")
    retailer_name = models.CharField(max_length=20,null=True,default=None)
    retailer_firmName = models.TextField(blank=True, null=True)
    retailer_contact_per = models.CharField(max_length=20,null=True,default=None)
    retailer_number = models.ManyToManyField(RetailerMobile,null=True, related_name='retailer_mobile',)
    retailer_wholeseller = models.ManyToManyField(Wholeseller,related_name='retailer_wholeseller',blank=True,null=True)
    retailer_agent = models.ForeignKey(Agent,on_delete=models.CASCADE ,related_name='retailer_agent',blank=True,null=True)
    retailer_altranate_number=PhoneNumberField(blank=True,null=True)
    retailer_plan = models.CharField(max_length=20, choices=RETAILER_PLAN, null=True)
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

    retailer_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    retailer_landmark = models.CharField(max_length=100, default=None, blank=True, null=True)
    retailer_pincode = models.IntegerField(null=True)
    retailer_image = models.ImageField(upload_to='images/retailer/', null=True)
    retailer_adharcard_no = models.CharField(max_length=12, default=None, blank=True, null=True)
    retailer_adhar_front_image = models.ImageField(upload_to="image/retailer/", null=True)
    retailer_adhar_back_image = models.ImageField(upload_to="image/retailer/", default=None, null=True)
    retailer_pancard_image = models.ImageField(upload_to="image/retailer/", default=None, null=True)
    retailer_pancard_no = models.CharField(max_length=50, default=None, blank=True, null=True)
    retailer_gst_no = models.CharField(max_length=50, default=None, blank=True, null=True)
    retailer_gst_image = models.ImageField(upload_to="image/retailer/", default=None, null=True)
    get_retailer_location_json_data = jsonfield.JSONField(default={}, null=True, )
    notification_status = models.CharField(max_length=20, choices=RETAILER_NOTIFICATION_STATUS, default="NEW", null=True)

    def __str__(self):
        return self.retailer_name


PAYMENT_TYPE = (
    ("CASH", "Cash"),
    ("CREDIT", "Credit"),
    ('UPI', 'UPI'),
    ('CHEQUE', 'Cheque'),
    ('NEFT/RTGS', 'NEFT/RTGS')
)
PAYMENT_STATUS = (
    ("PENDING", "Pending"),
    ("COMPLETED", "Completed")
)

ORDER_STATUS = (
    ("PENDING", 'Pending'),
    ("APPROVED", 'Approved'),
    ('REJECTED', 'Rejected'),
    ('INPROGRESS', 'InProgress'),
    ('SUCCESS', 'Success')
)
class PhotoOrder(models.Model):
    wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, related_name="photo_wholeseller", null=True,blank=True)
    order_image = models.ImageField(upload_to='images/photo_order/', null=True)
    retailer = models.ForeignKey(Retailer,related_name="retailer_order_photo", on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(max_length=8, unique=True, editable=False, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING", null=True)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    message = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_id()
        super(PhotoOrder, self).save(*args, **kwargs)

    def _generate_order_id(self):
        generated_id = str(uuid.uuid4().int)[:8]
        while PhotoOrder.objects.filter(order_id=generated_id).exists():
            generated_id = str(uuid.uuid4().int)[:8]
        return generated_id


class SubCart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_products", null=True, blank=True)
    qty = models.IntegerField(null=True)
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="carts_retailer", null=True, blank=True)
    used_in_cart = models.BooleanField(default=False)
    wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, related_name="cart_wholeseller", null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING", null=True)
    message = models.TextField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.pk)


class DeliveryAddress(models.Model):
    retailer = models.ForeignKey(Retailer, on_delete=models.CASCADE, related_name="delivery_addresses_retailer", null=True,
                                 blank=True)
    address = models.CharField(max_length=50, null=True)
    landmark = models.CharField(max_length=50, null=True)
    state = models.ForeignKey(State,on_delete=models.CASCADE, related_name='delivery_state',null=True, blank=True)
    city = models.ForeignKey(City,on_delete=models.CASCADE, related_name='delivery_city',null=True, blank=True)
    pincode = models.IntegerField(null=True)
    get_delivery_address_location_json_data = jsonfield.JSONField(default={}, null=True, )
    # payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE,  null=True)

    def __str__(self):
        return f"{self.retailer}'s Delivery Address: {self.address}, {self.landmark}, {self.city}, {self.state} - {self.pincode}"

class Cart(models.Model):
    cart_items = models.ManyToManyField(SubCart, related_name="carts", blank=True)
    order_id = models.CharField(max_length=8, unique=True, editable=False, null=True)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE, null=True)
    payment_amount = models.FloatField(null=True)
    payment_by_cash_paid_to = models.CharField(max_length=20,  null=True, blank=True)
    payment_by_cash_paid_by = models.CharField(max_length=20,  null=True, blank=True)
    payment_by_neft_rtgs_transaction_id = models.FloatField(null=True)
    payment_by_cheque_account_holdername = models.CharField(max_length=20, blank=True, null=True)
    payment_by_cheque_bank_account_number = models.IntegerField(null=True)
    payment_by_cheque_bank_cheque_number = models.IntegerField(null=True)
    payment_date = models.DateTimeField(default=datetime.now, blank=True)
    payment_image = models.ImageField(upload_to="image/retailer/payment_image", null=True)
    order_created_at = models.DateTimeField(default=datetime.now, blank=True)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, null=True)
    deliver_to = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, related_name='delivery_cart',null=True, blank=True)
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="PENDING", null=True)
    order_status_change_at = models.DateTimeField(blank=True)
    message = models.TextField(max_length=200, null=True, blank=True)


    def __str__(self):
        return str(self.order_id)

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self._generate_order_id()
        super(Cart, self).save(*args, **kwargs)

    def _generate_order_id(self):
        generated_id = str(uuid.uuid4().int)[:8]
        while Cart.objects.filter(order_id=generated_id).exists():
            generated_id = str(uuid.uuid4().int)[:8]
        return generated_id

class Favorites(models.Model):
    retailer = models.ForeignKey(Retailer, related_name="retailer_favorites", on_delete=models.CASCADE, null=True,blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="favorites_products", null=True, blank=True)

    def __str__(self):
        return f" {self.retailer} Favorite:- {self.product}"


class OutForDelivery(models.Model):
    retailer = models.ForeignKey(Retailer, related_name="retailer", on_delete=models.CASCADE, null=True,
                                 blank=True)
    wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, related_name="wholeseller", null=True,
                                    blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products", null=True,
                                blank=True)

    image = models.ImageField(upload_to="image/OutForDelivery/", default=None, null=True)
    bill_created_at = models.DateTimeField(default=datetime.now, blank=True)
    bill_number = models.IntegerField(null=True, blank=True)
    bill_amount = models.IntegerField(null=True)

    deliver_date = models.DateField(null=True)
    driver_number = PhoneNumberField(blank=True, null=True)
    driver_vehicle_number = models.CharField(max_length=50, null=True)

    current_address = models.CharField(max_length=50, null=True)
    is_delivery_address_same_as_current_address = models.BooleanField(default=True)

    landmark = models.CharField(max_length=50, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='outfordelivery_state', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='outfordelivery_city', null=True, blank=True)
    pincode = models.IntegerField(null=True)
    get_delivery_address_location_json_data = jsonfield.JSONField(default={}, null=True)

    def __str__(self):
        return str(self.bill_number)


class OrderStatus(models.Model):
    # order_id = models.CharField(max_length=10, blank=True)
    order_pending_date = models.DateTimeField(default=datetime.now, blank=True)
    order_accept_date = models.DateTimeField(default=datetime.now, blank=True)
    order_in_progress_date = models.DateTimeField(default=datetime.now, blank=True)
    order_ready_to_dispatch_date = models.DateTimeField(default=datetime.now, blank=True)
    order_for_delivery_date = models.DateTimeField(default=datetime.now, blank=True)
    delivered_at = models.DateTimeField(default=datetime.now, blank=True)


    def __str__(self):
        return str(self.order_id)