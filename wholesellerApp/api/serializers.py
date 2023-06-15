from rest_framework import serializers
from wholesellerApp.models import *
from bazaarApp.models import Bazaar
from retailerApp.models import Retailer
from productApp.models import Product
from drf_extra_fields.fields import Base64ImageField
from bazaarApp.api.serializers import BazaarSerializer
from locationApp.models import *
from planApp.models import Plan
from paymentApp.models import Payment
from masterApp.models import WholesellerType
from locationApp.api.serializers import *
# from locationApp.models import *


class WholesellerSerializer(serializers.ModelSerializer):
    wholeseller_adhar_front_image = Base64ImageField(required=False)
    wholeseller_adhar_back_image = Base64ImageField(required=False)
    wholeseller_pan_card_image = Base64ImageField(required=False)
    wholeseller_image = Base64ImageField(required=False)
    wholeseller_bazaar_data = serializers.SerializerMethodField()
    wholeseller_state_name = serializers.SerializerMethodField()
    wholeseller_district_name = serializers.SerializerMethodField()
    wholeseller_city_name = serializers.SerializerMethodField()
    wholeseller_plan_name = serializers.SerializerMethodField()
    wholeseller_payment_name = serializers.SerializerMethodField()
    wholeseller_type_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Wholeseller
        fields = '__all__'
        
    def get_wholeseller_state_name(self, obj):
        state = ""
        state_id = obj.wholeseller_state_id
        if state_id is not None:
            state = State.objects.filter(id=state_id).get().state
        return state
    
    def get_wholeseller_district_name(self, obj):
        district = ""
        district_id = obj.wholeseller_district_id
        if district_id is not None:
            district = District.objects.filter(id=district_id).get().district
        return district
    
    def get_wholeseller_city_name(self, obj):
        city = ""
        city_id = obj.wholeseller_city_id
        if city_id is not None:
            city = City.objects.filter(id=city_id).get().city
        return city
        
    def get_wholeseller_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data
    
    def get_wholeseller_plan_name(self, obj):
        plan = ""
        try :
            plan_id = obj.wholeseller_plan_id
        except:
            plan_id = None
        if plan_id is not None:
            plan = Plan.objects.filter(id=plan_id).get().plan_name
        return plan
    
    def get_wholeseller_payment_name(self, obj):
        payment = ""
        payment_id = obj.wholeseller_payment_id
        if payment_id is not None:
            payment = Payment.objects.filter(id=payment_id).get().payment_choice
        return payment
    
    def get_wholeseller_type_name(self, obj):
        wholeseller_type = ""
        wholeseller_type_id = obj.wholeseller_type_id
        if wholeseller_type_id is not None:
            wholeseller_type = WholesellerType.objects.filter(id=wholeseller_type_id).get().wholeseller_type_name
        return wholeseller_type
        
    def update(self, instance, validated_data):
        instance.wholeseller_adhar_front_image = validated_data.get(
            'wholeseller_adhar_front_image')
        instance.wholeseller_adhar_back_image = validated_data.get(
            'wholeseller_adhar_back_image')
        instance.wholeseller_pan_card_image = validated_data.get(
            'wholeseller_pan_card_image')
        instance.wholeseller_image = validated_data.get(
            'wholeseller_image')
        event = super().update(instance, validated_data)
        return event


class Wholeseller_bazzarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar"]


class WholesellerViewReportCityWiseSerializer(serializers.ModelSerializer):
    cities = serializers.SerializerMethodField(read_only=True)
    orders = serializers.SerializerMethodField(read_only=True)
    sales = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Wholeseller
        fields = ['id', 'cities', 'orders', 'sales']
        # fields = ['id', 'orders', 'sales']

    def get_cities(self, obj):
        city = obj.wholeseller_city.city
        return city

    def get_orders(self, obj):
        return 12000

    def get_sales(self, obj):
        return 10000


class WholesellerViewReportRetailerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    customer_id = serializers.SerializerMethodField()


class WholesellerDashboardTopRetailersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = "__all__"

class WholelsellerBazaarListSerializer(serializers.ModelSerializer):
    wholeseller_bazaar_data = serializers.SerializerMethodField()
    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar_data"]
        
    def get_wholeseller_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_bazaar.all()
        bazaar_names = []
        for bazaar in bazaar_ids:
            bazaar_name = Bazaar.objects.filter(id=bazaar.id).get().bazaar_name
            bazaar_data = {"bazaar_id":bazaar.id, "bazaar_name" : bazaar_name}
            bazaar_names.append(bazaar_data)
        return bazaar_names
    
class WholesellerBranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = "__all__"
        #fields = ['branch_name', 'manager_name', 'branch_phone']
        
class WholesellerBazaarProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = '__all__'
        
    def get_stock(self, obj):
        stock = obj.product_stocks
        if stock == None or 0:
            stocks = "Out of Stock"
        else:
            stocks = "Available"
        return stocks

class WholesellerBazaarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bazaar
        fields = "__all__"


#=====================   wholeseller agent


class WholesellerAgentSerializer(serializers.ModelSerializer):
    agent_image = Base64ImageField(required=False)
    agent_adhar_front_image = Base64ImageField(required=False)
    agent_adhar_back_image = Base64ImageField(required=False)
    product_upload_mrp_label_image = Base64ImageField(required=False)
    agent_pancard_image = Base64ImageField(required=False)
    agent_agency_name = serializers.SerializerMethodField()
    agent_bazaar_data = serializers.SerializerMethodField()
    wholeseller_agent_assigned_state_names = serializers.SerializerMethodField()
    wholeseller_agent_assigned_district_names = serializers.SerializerMethodField()
    wholeseller_agent_assigned_city_names = serializers.SerializerMethodField()
    wholeseller_agent_city_name = serializers.SerializerMethodField()
    agent_district_name = serializers.SerializerMethodField()
    agent_state_name = serializers.SerializerMethodField()



    class Meta:
        model = WholesellerAgent
        fields = '__all__'

    def get_agent_agency_name(self, obj):
        firm_name = ""
        agency_id = obj.agency_id
        if agency_id is not None:
            firm_name = Agency.objects.filter(id=agency_id).get().firm_name
        return firm_name

    def get_agent_state_name(self, obj):
        state = ""
        state_id = obj.wholeseller_agent_state_id
        if state_id is not None:
            state = State.objects.filter(id=state_id).get().state
        return state


    def get_agent_district_name(self, obj):
        district = ""
        district_id = obj.wholeseller_agent_district_id
        if district_id is not None:
            district = District.objects.filter(id=district_id).get().district
        return district


    def get_wholeseller_agent_city_name(self, obj):
        city = ""
        city_id = obj.wholeseller_agent_city_id
        if city_id is not None:
            city = City.objects.filter(id=city_id).get().city
        return city


    def get_agent_bazaar_data(self, obj):
        bazaar_ids = obj.wholeseller_agent_bazaar.all()
        bazaar = Bazaar.objects.filter(id__in=bazaar_ids)
        serializer = BazaarSerializer(bazaar, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_state_names(self, obj):
        state_ids = obj.wholeseller_agent_assigned_state.all()
        states = State.objects.filter(id__in=state_ids)
        serializer = StateSerializer(states, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_district_names(self, obj):
        district_ids = obj.wholeseller_agent_assigned_district.all()
        district = District.objects.filter(id__in=district_ids)
        serializer = DistrictSerializer(district, many=True)
        return serializer.data

    def get_wholeseller_agent_assigned_city_names(self, obj):
        city_ids = obj.wholeseller_agent_assigned_city.all()
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

