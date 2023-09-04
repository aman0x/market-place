from rest_framework import serializers
from planApp.models import *


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"
        

class FeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanFeatures
        fields = "__all__"

class RetailerPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerPlan
        fields = "__all__"