from django.db import models
from bazaarApp.models import Bazaar


class PlanFeatures(models.Model):
    projects=models.CharField(max_length=50,default=None,null=True)
    subscribers=models.CharField(max_length=50,default=None,null=True)

PLAN_CHOICE=(
    ("PAID","Paid"),
    ("FREE","Free")
)

class SelectCityState(models.Model):
    state=models.CharField(max_length=50,default=None,null=True)
    city=models.CharField(max_length=50,default=None,null=True)
    district=models.CharField(max_length=50,default=None,null=True)


class Plan(models.Model):
    plan_choice=models.CharField(max_length=20,choices=PLAN_CHOICE,default="Paid")
    firm_name=models.CharField(max_length=100,default=None,null=True)
    start_date=models.DateField(auto_now=False)
    start_time=models.TimeField(auto_now_add=False)
    end_date=models.DateField(auto_now=False)
    end_time=models.TimeField(auto_now_add=False)
    plan_features=models.ManyToManyField(PlanFeatures,related_name="plan_features")
    amount=models.IntegerField(null=True,default=None)
    branches=models.IntegerField(null=True,default=None)
    user_per_branch=models.IntegerField(null=True)
    bazaar=models.ManyToManyField(Bazaar,related_name="bazaar")
    select=models.ManyToManyField(SelectCityState)

def __str__(self):
    return self.firm_name
