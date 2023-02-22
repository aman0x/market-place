from django.contrib.auth.models import User,Group
from rest_framework import serializers
from planApp.models import Plan,AddPlan,PlanPaid
from bazaarApp.models import Bazaar


#class Planserializers(serializers.ModelSerializer):
 ##      model=Plan
   #     fields="__all__"

class AddPlanSerializers(serializers.ModelSerializer):
    class Meta:
        model=AddPlan
        fields="__all__"


class PlanPaidSerializers(serializers.ModelSerializer):
    class Meta:
        model=PlanPaid
        fields="__all__"

class PlanSerializers(serializers.HyperlinkedModelSerializer):
    Add_plan=AddPlanSerializers()
    Plan_paid=PlanPaidSerializers()

    class Meta:
        model=Plan
        fields="__all__"       


    

        