from django.contrib.auth.models import User, Group
from rest_framework import serializers
from agentApp.models import Agent, AgentCommisionRedeem
from drf_extra_fields.fields import Base64ImageField
from wholesellerApp.models import Wholeseller
from agencyApp.models import Agency
from bazaarApp.models import Bazaar
from bazaarApp.api.serializers import BazaarSerializer
from locationApp.api.serializers import *
from locationApp.models import *

# class AgentManageCommisionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ManageCommision
#         fields = '__all__'


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
    agent_assigned_state_names = serializers.SerializerMethodField()
    agent_assigned_district_names = serializers.SerializerMethodField()
    agent_assigned_city_names = serializers.SerializerMethodField()
    agent_city_name = serializers.SerializerMethodField()
    agent_district_name = serializers.SerializerMethodField()
    agent_state_name = serializers.SerializerMethodField()
    
    
    
    class Meta:
        model = Agent
        fields = '__all__'

    def get_agent_agency_name(self, obj):
        firm_name = ""
        agency_id = obj.agency_id
        if agency_id is not None:
            firm_name = Agency.objects.filter(id=agency_id).get().firm_name
        return firm_name
    
    def get_agent_state_name(self, obj):
        state = ""
        state_id = obj.agent_state_id
        if state_id is not None:
            state = State.objects.filter(id=state_id).get().state
        return state
        
        
    def get_agent_district_name(self, obj):
        district = ""
        district_id = obj.agent_district_id
        if district_id is not None:
            district = District.objects.filter(id=district_id).get().district
        return district

    
    def get_agent_city_name(self, obj):
        city = ""
        city_id = obj.agent_city_id
        if city_id is not None:
            city = City.objects.filter(id=city_id).get().city
        return city
        

    
    def get_agent_bazaar_data(self, obj):
        bazaar_ids = obj.agent_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data

    def get_agent_assigned_state_names(self, obj):
        state_ids = obj.agent_assigned_state.all()
        states = State.objects.filter(id__in=state_ids)
        serializer = StateSerializer(states, many=True)
        return serializer.data

    def get_agent_assigned_district_names(self, obj):
        district_ids = obj.agent_assigned_district.all()
        district = District.objects.filter(id__in=district_ids)
        serializer = DistrictSerializer(district, many=True)
        return serializer.data

    def get_agent_assigned_city_names(self, obj):
        city_ids = obj.agent_assigned_city.all()
        city = City.objects.filter(id__in=city_ids)
        serializer = CitySerializer(city, many=True)
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
