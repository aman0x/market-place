from django.db import models
from bazaarApp.models import Bazaar


class PlanFeatures(models.Model):
    projects=models.CharField(max_length=50,default=None,null=True)
    subscribes=models.CharField(max_length=50,default=None,null=True)

PLAN_CHOICE=(
    ("PAID","Paid"),
    ("FREE","Free")
)

class Plan(models.Model):
    plan_choice=models.CharField(max_length=20,choices=PLAN_CHOICE,default="Paid")
    firm_name=models.CharField(max_length=100,default=None,null=True)
    start_date=models.DateField(auto_now=False)
    start_time=models.TimeField(auto_now_add=False)
    end_date=models.DateField(auto_now=False)
    end_time=models.TimeField(auto_now_add=False)
    plan_features=models.ManyToManyField(PlanFeatures,related_name="plan_features")

    
class Paid(models.Model):
    plan=models.ForeignKey(Plan,on_delete=models.CASCADE)
    amount=models.IntegerField(null=True,default=None)
    branches=models.IntegerField(null=True,default=None)
    user_per_branch=models.IntegerField(null=True)
    bazaar=models.ForeignKey(Bazaar,on_delete=models.CASCADE)
    state=models.CharField(max_length=100,default=None,null=True)
    district=models.CharField(max_length=100,default=None,null=True)
    city=models.CharField(max_length=100,default=None,null=True)


