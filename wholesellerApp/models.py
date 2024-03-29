from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from locationApp.models import *
from planApp.models import Plan
from agencyApp.models import Agency
from paymentApp.models import Payment
from datetime import date
import jsonfield
from django.db import IntegrityError
from masterApp.models import WholesellerType
from datetime import datetime
from django.db import models
from subCategoryApp.models import SubCategory, Category, ParentCategory, Bazaar
from productApp.models import Product
from masterApp.models import RetailerType
from agentApp.models import Agent
from commonToall.common import *

# from offerApp.models import Offers

# WHOLESELLER_TYPE = (
#     ("INDIVIDUAL", "Individual"),
#     ("WHOLESELLER", "Wholeseller"),
#     ("SEMIWHOLESELLER","SemiWholeseller")
# )


class Wholeseller(models.Model):
    wholeseller_description = models.TextField(blank=True, null=True)
    wholeseller_name = models.CharField(max_length=200, blank=True)
    wholeseller_bazaar = models.ManyToManyField(Bazaar, 'wholeseller')
    wholeseller_plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="chooseplan", null=True, blank=True)
    wholeseller_payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='payment_detail', null=True, blank=True)
    wholeseller_type = models.ForeignKey(WholesellerType, on_delete=models.CASCADE, related_name="wholeseller_type")
    wholeseller_firm_name = models.CharField(max_length=20, null=True, default=None)
    wholeseller_agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='agent', blank=True, null=True)
    wholeseller_contact_per = models.CharField(max_length=20, null=True, default=None)
    wholeseller_number = PhoneNumberField(unique=True, blank=True, null=True)
    wholeseller_altranate_number = PhoneNumberField(blank=True, null=True)
    wholeseller_email_id = models.EmailField(max_length=25, null=True)
    wholeseller_adhar_no = models.CharField(max_length=12, null=True, default=None)
    wholeseller_gst_no = models.CharField(max_length=15, null=True, default=None)
    wholeseller_firm_pan_no = models.CharField(max_length=20, null=True, default=None)
    wholeseller_address = models.CharField(max_length=30, null=True, default=None)
    wholeseller_landmark = models.CharField(max_length=30, null=True, default=None)
    wholeseller_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='wholeseller_city')
    wholeseller_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='wholeseller_state')
    wholeseller_district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='wholeseller_district')
    wholeseller_pincode_no = models.IntegerField(null=True)
    wholeseller_adhar_front_image = models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d", null=True)
    wholeseller_adhar_back_image = models.ImageField(upload_to="adhar-image/wholeseller/%y/%m/%d", null=True)
    wholeseller_pan_card_image = models.ImageField(upload_to="pan-image/wholeseller/%y/%m/%d", null=True)
    wholeseller_image = models.ImageField(upload_to='images/wholeseller/', null=True)
    wholeseller_status = models.CharField(max_length=20, choices=WHOLESELLER_STATUS, default="CREATED")
    wholeseller_otp = models.IntegerField(blank=True, null=True)
    wholeseller_user = models.ForeignKey(User, related_name="wholeseller_user", on_delete=models.CASCADE, null=True, blank=True)
    wholeseller_active = models.BooleanField(default=False)
    get_wholeseller_location_json_data = jsonfield.JSONField(default={}, null=True, )
    created_at = models.DateField(auto_now_add=False, default=date.today, blank=True)

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
    branch_name = models.CharField(max_length=200, null=True)
    manager_name = models.CharField(max_length=200, null=True)
    branch_phone = PhoneNumberField(blank=True, unique=True, null=True)
    branch_otp = models.IntegerField(blank=True, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=300, null=True)
    landmark = models.CharField(max_length=300, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='branch_city')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='branch_state')
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='branch_district')
    pincode_no = models.IntegerField(null=True)
    created_at = models.DateField(auto_now_add=False, default=date.today, blank=True)
    branch_wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, related_name='branch_wholeseller')
    wholeseller_branch_user = models.ForeignKey(User, related_name="wholeseller_branch_user", on_delete=models.CASCADE, null=True, blank=True)
    main_branch = models.BooleanField(default=False,)
    def __str__(self):
        if self.branch_name != None:
            return self.branch_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the Branch object is being created for the first time
            if not Branch.objects.filter(branch_wholeseller=self.branch_wholeseller).exists():
                self.main_branch = True  # Set main_branch to True for the first branch
            try:
                user = User.objects.create_user(username=self.branch_phone, password='Test@!Test123')
                self.wholeseller_branch_user = user
            except IntegrityError:
                # If a user with the same username already exists, retrieve the existing user and update its fields
                user = User.objects.get(username=self.branch_phone)
                user.set_password('Test@!Test123')
                user.save()
                self.wholeseller_branch_user = user
        super().save(*args, **kwargs)



class Branch_Product(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='branch_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='branch_products')
    price = models.IntegerField(null=True)

class Branch_Category_Wise_Plan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='branch_category_wise_plan')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, related_name='branch_category')
    cash_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    cash_value = models.IntegerField(null=True)
    platinum_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    platinum_value = models.IntegerField(null=True)
    diamond_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    diamond_value = models.IntegerField(null=True)
    gold_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    gold_value = models.IntegerField(null=True)
    bronze_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    bronze_value = models.IntegerField(null=True)
    last_update_date = models.DateTimeField(default=datetime.now, blank=True)
    retailer_type = models.ManyToManyField(RetailerType, related_name="wholeseller_branch_category_wise_plan_retailer_type", blank=True)
        # (max_length=20, choices=CUSTOMER_TYPE, default="RETAILER")


class Branch_Sub_Category_Wise_Plan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='branch_sub_category_wise_plan')
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, related_name='branch_sub_category')
    cash_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    cash_value = models.IntegerField(null=True)
    platinum_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    platinum_value = models.IntegerField(null=True)
    diamond_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    diamond_value = models.IntegerField(null=True)
    gold_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    gold_value = models.IntegerField(null=True)
    bronze_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    bronze_value = models.IntegerField(null=True)
    last_update_date = models.DateTimeField(default=datetime.now, blank=True)
    retailer_type = models.ManyToManyField(RetailerType, related_name="wholeseller_branch_sub_category_wise_plan_retailer_type" )

class Branch_Item_Wise_Plan(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, related_name='branch_item_wise_plan')
    product = models.ManyToManyField(Product, related_name='branch_item')
    cash_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    cash_value = models.IntegerField(null=True)
    platinum_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    platinum_value = models.IntegerField(null=True)
    diamond_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    diamond_value = models.IntegerField(null=True)
    gold_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    gold_value = models.IntegerField(null=True)
    bronze_discount_type = models.CharField(max_length=20, choices=BRANCH_PLAN, default="PERCENTAGE")
    bronze_value = models.IntegerField(null=True)
    last_update_date = models.DateTimeField(default=datetime.now, blank=True)
    retailer_type = models.ManyToManyField(RetailerType, related_name="wholeseller_branch_item_wise_plan_retailer_type",blank=True)


class Branch_Product_Pricing(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='branch_product')
    new_base_price = models.IntegerField(null=True)
    last_update_date = models.DateTimeField(default=datetime.now, blank=True)



# -----------------------------Wholeseller agent ------------------


class WholesellerAgent(models.Model):
    wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, null=True, related_name='agent_wholeseller')
    wholeseller_agent_bazaar = models.ManyToManyField(Bazaar, related_name="wholeseller_agent")
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, null=True, related_name="wholeseller_agent_agency")
    wholeseller_agent_description = models.TextField(blank=True, null=True)
    wholeseller_agent_name = models.CharField(max_length=200)
    wholeseller_agent_type = models.CharField(max_length=170, choices=WHOLESELLER_AGENT_TYPE,default="WHOLESELLER_AGENT")
    wholeseller_agent_number = PhoneNumberField(unique=True, blank=True, null=True)
    wholeseller_agent_altranate_mobile_number = PhoneNumberField(blank=True, null=True)
    wholeseller_agent_email = models.EmailField(null=True)
    wholeseller_agent_gender = models.CharField(max_length=10, choices=WHOLESELLER_AGENT_GENDER, default="MALE")
    wholeseller_agent_date_of_birth = models.DateField(auto_now_add=False, null=True)
    wholeseller_agent_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    wholeseller_agent_landmark = models.CharField(max_length=100, default=None, blank=True, null=True)
    wholeseller_agent_state = models.ForeignKey(State, on_delete=models.CASCADE, null=True, related_name="wholeseller_agent_state")
    wholeseller_agent_city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, related_name="wholeseller_agent_city")
    wholeseller_agent_district = models.ForeignKey(District, on_delete=models.CASCADE, null=True, related_name="wholeseller_agent_district")
    wholeseller_agent_assigned_state = models.ManyToManyField(State, related_name="wholeseller_agent_assigned_state")
    wholeseller_agent_assigned_city = models.ManyToManyField(City, related_name="wholeseller_agent_assigned_city")
    wholeseller_agent_assigned_district = models.ManyToManyField(District, related_name="wholeseller_agent_assigned_district")
    wholeseller_agent_pincode = models.IntegerField(null=True)
    wholeseller_agent_commission_type = models.CharField(max_length=20, choices=WHOLESELLER_AGENT_COMMISSION_TYPE, default="PERCUSTOMER")
    wholeseller_agent_commission_value_type = models.CharField(max_length=20, choices=WHOLESELLER_AGENT_COMMISSION_VALUE_TYPE, default="AMOUNT")
    wholeseller_agent_commission_value = models.CharField(max_length=10, default=None, blank=True, null=True)
    wholeseller_agent_adharcard_no = models.CharField(max_length=12, default=None, blank=True, null=True)
    wholeseller_agent_adhar_front_image = models.ImageField(upload_to="image/wholeseller_agent/", null=True)
    wholeseller_agent_adhar_back_image = models.ImageField(upload_to="image/wholeseller_agent/", default=None, null=True)
    wholeseller_agent_pancard_image = models.ImageField(upload_to="image/wholeseller_agent/", default=None, null=True)
    wholeseller_agent_pancard_no = models.CharField(max_length=50, default=None, blank=True, null=True)
    wholeseller_agent_image = models.ImageField(upload_to='images/wholeseller_agent/', null=True)
    wholeseller_agent_status = models.CharField(max_length=20, choices=WHOLESELLER_AGENT_STATUS, default="CREATED")
    wholeseller_agent_otp = models.IntegerField(blank=True, null=True)
    wholeseller_agent_user = models.ForeignKey(User, related_name="wholeseller_agent_user", on_delete=models.CASCADE, null=True, blank=True)
    is_active = ()
    wholeseller_agent_active = models.BooleanField(default=False)
    get_wholeseller_agent_location_json_data = jsonfield.JSONField(default={}, null=True, )

    # wholeseller_agent_date_of_creation = models.DateTimeField(auto_now_add=False,null=True,blank=True)

    def __str__(self):
        return self.wholeseller_agent_name

    def save(self, *args, **kwargs):
        if not self.pk:
            # If the Agent object is being created for the first time
            try:
                user = User.objects.create_user(
                    username=self.wholeseller_agent_number, password='Test@!Test123')
                self.wholeseller_agent_user = user
            except IntegrityError:
                # If a user with the same username already exists, retrieve the existing user and update its fields
                user = User.objects.get(username=self.wholeseller_agent_number)
                user.set_password('Test@!Test123')
                user.save()
                self.wholeseller_agent_user = user
        super().save(*args, **kwargs)


# --------------------------------wholeseller order
ORDER_BY = (
    ("ADMIN", "admin"),
    ("PHOTO", "photo"),
    ("RETAILER", "retailer")
)

ORDER_TYPE = (
    ("CASH", "Cash"),
    ("CREDIT", "Credit")
)

PAYMENT_STATUS = (
    ("PAID", "Paid"),
    ("PENDING", "Pending")
)

ORDER_STATUS = (
    ("ORDERACCEPTED", "Order Accepted"),
    ("PENDING", "Order Pending "),
    ("CANCELED", "Cancelled"),
    ("INPROGRESS", "In Progress"),
)
class Order(models.Model):
    date = models.DateField()
    # order_id = models.CharField(max_length=100)
    firm_name = models.CharField(max_length=100)
    retailer_type = models.ManyToManyField(RetailerType, related_name="orders_retailer_type" )
    phone = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='orders_city')
    ordered_by = models.CharField(max_length=20, choices=ORDER_BY, default="RETAILER")
    amount = models.IntegerField()
    order_type = models.CharField(max_length=20, choices=ORDER_TYPE, default="CASH")
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default="PENDING")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS, default="INPROGRESS")

    def __str__(self):
        return str(self.pk)
class EditOrder(models.Model):
    order_id = models.ForeignKey(Order, related_name="editorder_order_id", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='orders_product')
    offer = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.order_id

#----- offer---------------


DISCOUNT_BY_TYPE = (
    ("PERCENTAGE", "Percentage"),
    ("AMOUNT", "Amount")
)

CREATE_OFFER_BY_TYPE = (
    ("GROUP", "Group"),
    ("CATEGORY", "Category"),
    ("SUBCATEGORY", "SubCategory"),
    ("PRODUCT", "Item")
)

PLAN = (
    ('CASH', 'Cash'),
    ('PLATINUM', 'Platinum'),
    ('DIAMOND', 'Diamond'),
    ('GOLD', 'Gold'),
    ('BRONZE', 'Bronze')
)

class Offers(models.Model):
    create_offer_by_item = models.CharField(max_length=20, choices=CREATE_OFFER_BY_TYPE, default="GROUP")
    category_group = models.ForeignKey(ParentCategory, on_delete=models.CASCADE,null=True,related_name='offer')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name='offer')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True, related_name='offer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, related_name='offer')

    offer_base_price = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    offer_discount_value_type = models.CharField(max_length=20,choices=DISCOUNT_BY_TYPE,default="PERCENTAGE")
    offer_discount_value = models.CharField(max_length=20, null=True, default=None)
    offer_discounted_price = models.CharField(max_length=20, null=True, default=None)
    offer_coupon_code = models.CharField(max_length=200, null=True, blank=True, default='')
    offer_start_date = models.DateField(default=datetime.now, blank=True)
    offer_end_date = models.DateField(default=datetime.now, blank=True)
    offer_min_qty = models.IntegerField()
    offer_max_qty = models.IntegerField()

    wholeseller = models.ForeignKey(Wholeseller, on_delete=models.CASCADE, related_name='offer')
    wholeseller_agent = models.ForeignKey(WholesellerAgent, on_delete=models.CASCADE, related_name='offer')

    offer_image = models.ImageField(upload_to="image/offer/", null=True)
    offer_active = models.BooleanField(default=True)
    offer_for = models.CharField(max_length=200)
    customer_type = models.ForeignKey(RetailerType, on_delete=models.CASCADE, null=True,related_name='offer')
    customer = models.CharField(max_length=20, choices=PLAN, default="CASH")


    class Meta:
        verbose_name_plural = "offers"

    def __str__(self):
        if self.product is not None:
            return self.product
        else:
            return "None"
