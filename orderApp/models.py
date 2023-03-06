from django.db import models
from productApp.models import Product

class Orders(models.Model):
    order_date=models.DateField(auto_now_add=False)
    order_time=models.TimeField(auto_now_add=False)
    #payment=models.ForeignKey(UserPayment,on_delete=models.CASCADE)
    Product=models.ManyToManyField(Product)
    

    def __str__(self):
        return self.payment