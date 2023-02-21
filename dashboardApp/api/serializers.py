from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bazaarApp.models import Bazaar

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class BazaarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bazaar
        fields = ['url', 'name', 'description', 'is_active']

class SummarySerializer(serializers.HyperlinkedModelSerializer):
    bazaars = serializers.SerializerMethodField(read_only=True)
    wholesellers = serializers.SerializerMethodField(read_only=True)
    revenue = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    commission = serializers.SerializerMethodField(read_only=True)
    customers = serializers.SerializerMethodField(read_only=True)
    class Meta:

        model = Bazaar
        fields = ['bazaars','wholesellers','revenue','bills','agents','commission','customers']

    def get_bazaars(self, task):
        return '15'
    
    def get_wholesellers(self, task):
        return '60'
    
    def get_revenue(self, task):
        return '194000'
    
    def get_bills(self, task):
        return '56'
    
    def get_agents(self, task):
        return '52'
    
    def get_commission(self, task):
        return '45000'
    
    def get_customers(self, task):
        return '1100'

class BazaarReportSerializer(serializers.HyperlinkedModelSerializer):
    wholesellers = serializers.SerializerMethodField(read_only=True)
    revenue = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    commission = serializers.SerializerMethodField(read_only=True)
    customers = serializers.SerializerMethodField(read_only=True)
    class Meta:

        model = Bazaar
        fields = ['wholesellers','revenue','bills','agents','commission','customers']
    
    def get_wholesellers(self, task):
        return '55'
    
    def get_revenue(self, task):
        return '189000'
    
    def get_bills(self, task):
        return '54'
    
    def get_agents(self, task):
        return '51'
    
    def get_commission(self, task):
        return '46000'
    
    def get_customers(self, task):
        return '1000'
    
class PlansSerializer(serializers.HyperlinkedModelSerializer):
    plans = serializers.SerializerMethodField(read_only=True)
    subscribers = serializers.SerializerMethodField(read_only=True)
    revenue = serializers.SerializerMethodField(read_only=True)
    class Meta:

        model = Bazaar
        fields = ['plans','subscribers','revenue']
    
    def get_plans(self, task):
        return '8'

    def get_subscribers(self, task):
        return '10000'
    
    def get_revenue(self, task):
        return '150000'