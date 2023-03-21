from django.db import models
from bazaarApp.models import Bazaar
from locationApp.models import *
import datetime

class PlanFeatures(models.Model):
    feature = models.CharField(max_length=50, default=None, null=True)

    def __str__(self):
        return self.feature

PLAN_CHOICE = (
    ("PAID", "Paid"),
    ("FREE", "Free")
)

class Plan(models.Model):
    plan_choice = models.CharField(
        max_length=20, choices=PLAN_CHOICE, default="Paid")
    firm_name = models.CharField(max_length=100, default=None, null=True)
    start_date = models.DateField( default=datetime.date.today)
    start_time = models.TimeField(
         default=datetime.time(10, 0))
    end_date = models.DateField( default=datetime.date.today)
    end_time = models.TimeField( default=datetime.time(10, 0))
    amount = models.IntegerField(null=True, default=None)
    branches = models.IntegerField(null=True, default=None)
    user_per_branch = models.IntegerField(null=True)
    bazaar = models.ManyToManyField(Bazaar, related_name="bazaar")
    state = models.ManyToManyField(State, related_name="plan_state")
    city = models.ManyToManyField(City, related_name="plan_city")
    district = models.ManyToManyField(District, related_name="plan_district")
    plan_features = models.ManyToManyField(
        PlanFeatures,  related_name="plan_features")

    
    def __str__(self):
        return self.firm_name