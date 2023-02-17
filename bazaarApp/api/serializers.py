from django.contrib.auth.models import User, Group
from rest_framework import serializers
from bazaarApp.models import Bazaar
from agentApp.models import Agent
from agentApp.api.serializers import AgentSerializer
from wholesellerApp.api.serializers import WholesellerSerializer

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class BazaarAgentSerializer(serializers.ModelSerializer):
    agent = AgentSerializer(many=True, read_only=True)
    class Meta:
        model = Bazaar
        fields = "__all__"

class BazaarWholesellerSerializer(serializers.ModelSerializer):
    wholeseller = WholesellerSerializer(many=True, read_only=True)
    class Meta:
        model = Bazaar
        fields = "__all__"

class BazaarProductSerializer(serializers.ModelSerializer):
    agent = serializers.StringRelatedField(many=True)
    class Meta:
        model = Bazaar
        fields = "__all__"

    

class BazaarSerializer(serializers.HyperlinkedModelSerializer):
    wholesellers = serializers.SerializerMethodField(read_only=True)
    agents = serializers.SerializerMethodField(read_only=True)
    states = serializers.SerializerMethodField(read_only=True)
    earnings = serializers.SerializerMethodField(read_only=True)
    bills = serializers.SerializerMethodField(read_only=True)
    class Meta:

        model = Bazaar
        fields = '__all__'
        
    def get_wholesellers(self, task):
        return '20'
    
    def get_agents(self, task):
        return '13'
    
    def get_states(self, task):
        return '2'
    
    def get_earnings(self, task):
        return '154000'
    
    def get_bills(self, task):
        return '52'