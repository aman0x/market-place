from rest_framework import serializers
from wholesellerApp.models import Wholeseller
from wholesellerApp.models import Branch
from bazaarApp.models import Bazaar
from retailerApp.models import Retailer
from productApp.models import Product
from parentCategoryApp.models import ParentCategory
import requests
from django.http import JsonResponse
from drf_extra_fields.fields import Base64ImageField
from bazaarApp.api.serializers import BazaarSerializer


class WholesellerSerializer(serializers.ModelSerializer):
    wholeseller_adhar_front_image = Base64ImageField(required=False)
    wholeseller_adhar_back_image = Base64ImageField(required=False)
    wholeseller_pan_card_image = Base64ImageField(required=False)
    wholeseller_image = Base64ImageField(required=False)
    
    class Meta:
        model = Wholeseller
        fields = '__all__'
        
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


class WholesellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = '__all__'


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
    wholeseller_bazaar_name = serializers.SerializerMethodField()
    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar_name", "wholeseller_bazaar"]
        
    def get_wholeseller_bazaar_name(self, obj):
        bazaar_ids = obj.wholeseller_bazaar.all()
        bazaar_names = []
        for bazaar in bazaar_ids:
            bazaar_name = Bazaar.objects.filter(id=bazaar.id).get().bazaar_name
            bazaar_names.append(bazaar_name)
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
