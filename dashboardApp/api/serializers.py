from rest_framework import serializers
from bazaarApp.models import Bazaar
from datetime import timedelta



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
        
    def get_plan_name(self, tsk):
        return 'plan-name'
    
    def get_bazaar(self, obj):
        return obj.bazaar.all().values_list('bazaar_name',flat=True)
    
    def get_state(self, obj):
        return obj.state.all().values_list('bazaar_state',flat=True)
    
    def get_district(self, obj):
        return obj.district.all().values_list('bazaar_district',flat=True)
    
    def get_city(self, obj):
        return obj.city.all().values_list('bazaar_city',flat=True)
    
    def get_duration(self, obj):
        duration = obj.end_date - obj.start_date
        duration_days = duration / timedelta(days=1)
        return f"{int(duration_days)} days" 
    
    def get_plan_price(self, obj):
        return obj.amount
    
    def get_subscribers_active(self, obj):
       return 

        return '12000'
       #return obj.plan_features_subscriber.subscribers
    
    def get_subscribers_expired(self, obj):
        return '100'
    
    def get_subscribers_deactivated(self, obj):
        return '100'
    
    def get_revenue_generated(self, obj):
        return '1500'


class BazaarListSerializer(serializers.ModelSerializer):

    class Meta:

        model = Bazaar
        fields = '__all__'
