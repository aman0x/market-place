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


class HighScoreSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        return {
            'score': instance.score,
            'player_name': instance.player_name
        }


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