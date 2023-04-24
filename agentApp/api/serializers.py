from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, ManageCommision, AgentCommisionRedeem
from drf_extra_fields.fields import Base64ImageField
from wholesellerApp.models import Wholeseller
from agencyApp.models import Agency
from bazaarApp.models import Bazaar
from bazaarApp.api.serializers import BazaarSerializer

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
    agent_agency_name = serializers.SerializerMethodField()
    agent_bazaar_data = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = Agent
        fields = '__all__'

    def get_agent_agency_name(self, obj):
        firm_name = ""
        agency_id = obj.agency_id
        if agency_id is not None:
            firm_name = Agency.objects.filter(id=agency_id).get().firm_name
        return firm_name
    
    def get_agent_bazaar_data(self, obj):
        bazaar_ids = obj.agent_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data

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
