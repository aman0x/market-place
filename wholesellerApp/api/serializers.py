from rest_framework import serializers
from wholesellerApp.models import Wholeseller
import requests


class WholesellerSerializerAll(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = '__all__'


class WholesellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = '__all__'


class Wholeseller_bazzarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = ["wholeseller_bazaar"]
