from django.db import models
from bazaarApp.models import Bazaar
from locationApp.models import *


class PlanFeaturesProject(models.Model):
    projects = models.CharField(max_length=50, default=None, null=True)


class PlanFeaturesSubscribers(models.Model):
    subscribers = models.CharField(max_length=50, default=None, null=True)


PLAN_CHOICE = (
    ("PAID", "Paid"),
    ("FREE", "Free")
)


class Plan(models.Model):
    plan_choice = models.CharField(
        max_length=20, choices=PLAN_CHOICE, default="Paid")
    firm_name = models.CharField(max_length=100, default=None, null=True)
    start_date = models.DateField(auto_now=False)
    start_time = models.TimeField(auto_now_add=False)
    end_date = models.DateField(auto_now=False)
    end_time = models.TimeField(auto_now_add=False)
    amount = models.IntegerField(null=True, default=None)
    branches = models.IntegerField(null=True, default=None)
    user_per_branch = models.IntegerField(null=True)
    bazaar = models.ManyToManyField(Bazaar, related_name="bazaar")
    state = models.ManyToManyField(State, related_name="plan_state")
    city = models.ManyToManyField(City, related_name="plan_city")
    district = models.ManyToManyField(District, related_name="plan_district")
    plan_features_project = models.ForeignKey(
        PlanFeaturesProject, on_delete=models.CASCADE)
    plan_features_subscriber = models.ForeignKey(
        PlanFeaturesSubscribers, on_delete=models.CASCADE)


def __str__(self):
    return self.firm_name
