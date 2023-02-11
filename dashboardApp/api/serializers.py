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
