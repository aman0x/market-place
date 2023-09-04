from rest_framework import serializers
from locationApp.models import *
from bazaarApp.models import Bazaar



class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model=State
        fields="__all__"

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = "__all__"

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"

class DistrictGroupBySerializer(serializers.ModelSerializer):
    district = serializers.SerializerMethodField()
    state_name = serializers.ReadOnlyField(source='state.state')
    class Meta:
        model = District
        fields = ['state', 'state_name', 'district']
    def get_district(self, obj):
        return list(District.objects.filter(state= obj.state).values("id", "district"))

class CityGroupBySerializer(serializers.ModelSerializer):
    city = serializers.SerializerMethodField()
    district_name = serializers.ReadOnlyField(source='district.district')
    class Meta:
        model = City
        fields = ['district', 'district_name', 'city']
    def get_city(self, obj):
        return list(City.objects.filter(district= obj.district).values("id", "city"))
    
class StateGroupByBazaarSerializer(serializers.ModelSerializer):
    bazaar = serializers.ReadOnlyField(source='id')
    class Meta:
        model = Bazaar
        fields = ['bazaar','bazaar_name','bazaar_state']