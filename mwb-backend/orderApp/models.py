from django.db import models
from productApp.models import Product
from locationApp.models import City
from masterApp.models import RetailerType

ORDER_TYPE = (
    ("CASH", "Male"),
    ("CREDIT", "Female")
)

class Orders(models.Model):
    order_date = models.DateField(auto_now_add=False)
    order_time = models.TimeField(auto_now_add=False)
    # payment=models.ForeignKey(UserPayment,on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name='order_product')
    city = models.ForeignKey(
        City,on_delete=models.CASCADE, related_name="order_city", null=True ,default=None)
    retailer_type = models.ForeignKey(
        RetailerType, on_delete=models.CASCADE, related_name="order_retailer_type", null=True , default=None)
    amount = models.IntegerField(null=True)
    order_type = models.CharField(max_length=20,choices=ORDER_TYPE, default="CREDIT")

    def __str__(self):
        return self.payment