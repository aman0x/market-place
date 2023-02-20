from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, ManageCommision
from bazaarApp.models import Bazaar



class AgentManageCommisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageCommision
        fields = '__all__'
    



class AgentSerializer(serializers.HyperlinkedModelSerializer):
    agent_commision = AgentManageCommisionSerializer()

    

    class Meta:
        model = Agent
        fields = '__all__'
    
    
    
    def create(self, validated_data):
        agent_commision_data = validated_data.pop('agent_commision')
        agent_bazaar = validated_data.pop('agent_bazaar')
        
        for bazaar in agent_bazaar:
            Agent.agent_bazaar.add(bazaar)
        agent_commision.objects.create(
            user=agent_bazaar, **agent_commision_data)
        return agent_bazaar

    def update(self, instance, validated_data):
        status = validated_data.pop('agent_commision')
        instance.status_id = status.id
        # ... plus any other fields you may want to update
        return instance
    
