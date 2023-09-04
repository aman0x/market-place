from orderApp.models import Orders
from rest_framework import serializers


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Orders
        fields="__all__"

        