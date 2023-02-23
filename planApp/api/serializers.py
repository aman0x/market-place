from django.contrib.auth.models import User,Group
from rest_framework import serializers
from planApp.models import Plan,PlanFeatures,Paid

class PaidSerializers(serializers.ModelSerializer):
    class Meta:
        model=Paid
        fields="__all__"


class PlanFeatureSerializers(serializers.ModelSerializer):
    class Meta:
        model=PlanFeatures
        fields="__all__"


class PlanSerializers(serializers.HyperlinkedModelSerializer):
    plan_paid=PaidSerializers()
    plan_features=PlanFeatureSerializers()
    class Meta:
        model=Plan
        fields="__all__"




        