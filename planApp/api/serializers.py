from django.contrib.auth.models import User,Group
from rest_framework import serializers
from planApp.models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"

# class PlanFreeSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Plan
#         fields = ['plan_choice','firm_name','start_date',
#                   'start_time','end_date','end_time',
#                   'plan_features']
    
#     def to_representation(self, instance):
#         data =  super().to_representation(instance)
#         data['plan_choice'] = 'free'
#         return data

# class PlanPaidSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Plan
#         fields = ['firm_name','start_date',
#                   'start_time','end_date','end_time','amount','branches',
#                   'user_per_branch','bazaar','state','city','district',
#                   'plan_features']

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeatures
        fields = "__all__"