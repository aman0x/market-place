from rest_framework import serializers
from retailerApp.models import Retailer
from wholesellerApp.models import Wholeseller
from wholesellerApp.api.serializers import WholesellerSerializer


class RetailerSerializer(serializers.ModelSerializer):
    wholeseller_details = serializers.SerializerMethodField()
    class Meta:
        model = Retailer
        fields = '__all__'

    def get_wholeseller_details(self, obj):
        wholesellers = obj.retailer_wholeseller.all().order_by("id")
        wholeseller_data = WholesellerSerializer(wholesellers, many=True).data
        return wholeseller_data