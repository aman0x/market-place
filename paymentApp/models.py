from django.db import models
from planApp.models import Plan

PAYMENT_CHOICES=(
    ("CASH","Cash"),
    ("ONLINEPAYMENT","OnlinePayment"),
)

class Payment(models.Model):
    plan_name=models.ForeignKey(Plan,on_delete=models.CASCADE)
    payment_choice=models.CharField(max_length=13,choices=PAYMENT_CHOICES,default="CASH")
    paid_to=models.CharField(max_length=20,null=True,default=None)
    amount=models.IntegerField(null=True)
    payment_date=models.DateField(auto_now_add=True)


    def __str__(self):
        return self.payment_choice

