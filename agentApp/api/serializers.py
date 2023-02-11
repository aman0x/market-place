from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent



class AgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'
