from django.contrib.auth.models import User,Group
from rest_framework import serializers
from planApp.models import *


class PlanFreeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Plan
        fields = ['plan_choice','firm_name','start_date',
                  'start_time','end_date','end_time',
                  'plan_features_project','plan_features_subscriber']
    
    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['plan_choice'] = 'free'
        return data

class PlanPaidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['firm_name','start_date',
                  'start_time','end_date','end_time','amount','branches',
                  'user_per_branch','bazaar','state','city','district',
                  'plan_features_project','plan_features_subscriber']

class FeaturesProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeaturesProject
        fields = "__all__"

class FeaturesSubscribersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeaturesSubscribers
        fields = "__all__"