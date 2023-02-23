
from rest_framework import serializers
from bazaarApp.models import Bazaar


class SummarySerializer(serializers.Serializer):
    bazaar = serializers.IntegerField(read_only=True)
    wholeseller = serializers.IntegerField(read_only=True)
    revenue = serializers.IntegerField(read_only=True)
    bill = serializers.IntegerField(read_only=True)
    agent = serializers.IntegerField(read_only=True)
    commission = serializers.IntegerField(read_only=True)
    customer = serializers.IntegerField(read_only=True)
    

class BazaarReportSerializer(serializers.Serializer):
    wholeseller = serializers.IntegerField(read_only=True)
    revenue = serializers.IntegerField(read_only=True)
    bill = serializers.IntegerField(read_only=True)
    agent = serializers.IntegerField(read_only=True)
    commission = serializers.IntegerField(read_only=True)
    customer = serializers.IntegerField(read_only=True)
    

class PlansSerializer(serializers.Serializer):
    plan = serializers.IntegerField(read_only=True)
    subscriber = serializers.IntegerField(read_only=True)
    revenue = serializers.IntegerField(read_only=True)