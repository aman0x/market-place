from rest_framework import serializers
from wholesellerApp.models import Wholeseller
from bazaarApp.models import Bazaar
from retailerApp.models import Retailer
from parentCategoryApp.models import ParentCategory
import requests
from django.http import JsonResponse


class WholesellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = '__all__'


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
