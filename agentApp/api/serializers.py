from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, ManageCommision, AgentCommisionRedeem
from drf_extra_fields.fields import Base64ImageField
from wholesellerApp.models import Wholeseller


class AgentManageCommisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManageCommision
        fields = '__all__'


class AgentWalletSerializer(serializers.Serializer):

    total_amount_earned = serializers.IntegerField()
    total_amount_withdrawn = serializers.IntegerField()
    agent_balance= serializers.IntegerField()
    agent_withdrawable_balance = serializers.IntegerField()


class AgentSerializer(serializers.ModelSerializer):
    agent_image = Base64ImageField(required=False)
    agent_adhar_front_image = Base64ImageField(required=False)
    agent_adhar_back_image = Base64ImageField(required=False)
    product_upload_mrp_label_image = Base64ImageField(required=False)
    agent_pancard_image = Base64ImageField(required=False)
    
    class Meta:
        model = Agent
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.agent_image = validated_data.get(
            'agent_image')
        instance.agent_adhar_front_image = validated_data.get(
            'agent_adhar_front_image')
        instance.agent_adhar_back_image = validated_data.get(
            'agent_adhar_back_image')
        instance.agent_pancard_image = validated_data.get(
            'agent_pancard_image')
        event = super().update(instance, validated_data)
        return event


class AgentCommisionRedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model=AgentCommisionRedeem
        fields= "__all__"


class WholsellerListSerializers(serializers.ModelSerializer):

    class Meta:
        model=Wholeseller
        fields= "__all__"
