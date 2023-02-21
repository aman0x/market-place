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


    def create(self,validated_data):
        add_plan_data = validated_data.pop("Add_plan")
        plan_paid_data = validated_data.pop("Plan_paid")
        add_plan = AddPlan.objects.create(**add_plan_data)
        plan_paid = PlanPaid.objects.create(**plan_paid_data)
        plan = Plan.objects.create(ADD_new_plan=add_plan,plan_paid=plan_paid,**validated_data)
        return plan



    
    
    def update(self,instance,validated_data):
        add_plan_data = validated_data.pop("Add_plan", None)
        plan_paid_data = validated_data.pop("Plan_paid", None)
        if add_plan_data:
                 plan_paid = instance.plan_paid
                 plan_paid.First_name = plan_paid_data.get("First_name", plan_paid.First_name)
                 plan_paid.Amount = plan_paid_data.get("Amount", plan_paid.Amount)
                 plan_paid.User_per_branch = plan_paid_data.get("User_per_branch", plan_paid.User_per_branch)
                 plan_paid.save()

        instance.Plan_Title = validated_data.get("Plan_Title", instance.Plan_Title)
        instance.Start_Time = validated_data.get("Start_Time", instance.Start_Time)
        instance.End_Time = validated_data.get("End_Time", instance.End_Time)
        instance.Branches = validated_data.get("Branches", instance.Branches)
        instance.bazaar = validated_data.get("bazaar", instance.bazaar)
        instance.state = validated_data.get("state", instance.state)
        instance.District = validated_data.get("District", instance.District)
        instance.City = validated_data.get("City", instance.City)
        instance.Price = validated_data.get("Price", instance.Price)
        instance.save()
            





        