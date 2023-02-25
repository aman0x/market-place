from django.contrib.auth.models import User,Group
from rest_framework import serializers
from planApp.models import *


class PlanFreeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = "__all__"


<<<<<<< Updated upstream
class PlanSerializers(serializers.HyperlinkedModelSerializer):
    plan_features=PlanFeatureSerializers(read_only=True)
=======
class PlanFreeSerializer(serializers.ModelSerializer):
>>>>>>> Stashed changes
    class Meta:
        model =Plan 
        fields = "__all__"