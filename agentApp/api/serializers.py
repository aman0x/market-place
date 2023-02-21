from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, ManageCommision
from bazaarApp.models import Bazaar
from agencyApp.models import Agency


class AgentManageCommisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageCommision
        fields = '__all__'
    

class AgentBazaarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bazaar
        fields = '__all__'


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'

