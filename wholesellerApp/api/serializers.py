from rest_framework import serializers
from wholesellerApp.models import Wholeseller


class WholesellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wholeseller
        fields = '__all__'



