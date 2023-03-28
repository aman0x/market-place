from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, ManageCommision,AgentCommisionRedeem


class AgentManageCommisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageCommision
        fields = '__all__'
    


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class AgentCommisionRedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model=AgentCommisionRedeem
        fields= "__all__"



class NewRequestSerializers(serializers.Serializer):
    firm_name_1=serializers.SerializerMethodField(read_only=True)

    def get_firm_name(self):
        return "vijay"


