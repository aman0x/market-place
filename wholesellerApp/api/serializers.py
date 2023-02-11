from rest_framework import serializers
from wholesellerApp.models import Wholeseller


class WholesellerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wholeseller
        fields = ['url', 'wholeseller_name']
