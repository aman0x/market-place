
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

class PlanListSerializer(serializers.ModelSerializer):
    plan_name = serializers.SerializerMethodField(read_only=True)
    bazaar = serializers.SerializerMethodField(read_only=True)
    state = serializers.SerializerMethodField(read_only=True)
    district = serializers.SerializerMethodField(read_only=True)
    city = serializers.SerializerMethodField(read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)
    plan_price = serializers.SerializerMethodField(read_only=True)
    subscribers_active = serializers.SerializerMethodField(read_only=True)
    subscribers_expired = serializers.SerializerMethodField(read_only=True)
    subscribers_deactivated = serializers.SerializerMethodField(read_only=True)
    revenue_generated = serializers.SerializerMethodField(read_only=True)
    class Meta:

        model = Bazaar
        fields = ['plan_name','bazaar','state','district',
                  'city','duration','plan_price','subscribers_active',
                  'subscribers_expired','subscribers_deactivated','revenue_generated']
        
    def get_plan_name(self, task):
        return 'Plan Name'
    
    def get_bazaar(self, task):
        return 'Electronic Bazaar, Computer Bazaar'
    
    def get_state(self, task):
        return 'UP,Delhi'
    
    def get_district(self, task):
        return 'GB Nagar Ghaziabad, Noida'
    
    def get_city(self, task):
        return 'Ghaziabad, Noida'
    
    def get_duration(self, task):
        return '7days'
    
    def get_plan_price(self, task):
        return 10000
    
    def get_subscribers_active(self, task):
        return 141
    
    def get_subscribers_expired(self, task):
        return 14
    
    def get_subscribers_deactivated(self, task):
        return 7
    
    def get_revenue_generated(self, task):
        return 12000

class BazaarListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bazaar
        fields = '__all__'
