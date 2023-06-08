from django.db import models

# Create your models here.
from django.conf import settings
from datetime import datetime
from django.db import models
from subCategoryApp.models import SubCategory, Category, ParentCategory, Bazaar
from productApp.models import Product
from masterApp.models import RetailerType
from retailerApp.models import Retailer
from wholesellerApp.models import Wholeseller, Agent


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

class Offers(models.Model):
    create_offer_by_item = models.CharField(max_length=20, choices=CREATE_OFFER_BY_TYPE, default="GROUP")
    category_group = models.ForeignKey(ParentCategory, on_delete=models.CASCADE,null=True,
                                       related_name='offer_product_parent_category')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name='offer_product_category')
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,null=True, related_name='offer_product_subcategory')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True, related_name='offer_product_name')

    offer_base_price = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    offer_discount_value_type = models.CharField(max_length=20,
                                                 choices=DISCOUNT_BY_TYPE,
                                                 default="PERCENTAGE")
    offer_discount_value = models.CharField(max_length=20, null=True, default=None)
    offer_discounted_price = models.CharField(max_length=20, null=True, default=None)
    #offer_coupon_code = models.CharField(max_length=200)
    offer_start_date = models.DateField(default=datetime.now, blank=True)
    offer_end_date = models.DateField(default=datetime.now, blank=True)
    offer_min_qty = models.IntegerField()
    offer_max_qty = models.IntegerField()

    # Wholeseller = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='offer_wholeseller_name')
    # wholeseller_agent = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name='offer_agent')

    offer_image = models.ImageField(upload_to="offer-image/offer/%y/%m/%d", null=True)
    offer_active = models.BooleanField(default=True)
    offer_for = models.CharField(max_length=200)
    customer_type = models.ForeignKey(RetailerType, on_delete=models.CASCADE, null=True,
                                       related_name='offer_customer_type')
    customer = models.ForeignKey(Retailer, on_delete=models.CASCADE, null=True,
                                       related_name='offer_customer')


    class Meta:
        verbose_name_plural = "offers"

    def __str__(self):
        if self.product is not None:
            return self.product
        else:
            return "None"
