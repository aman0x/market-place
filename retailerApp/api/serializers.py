from rest_framework import serializers
from retailerApp.models import Retailer
import requests


class RetailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retailer
        fields = '__all__'

