from rest_framework import serializers
from masterApp.models import *


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class WholesellerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WholesellerType
        fields = "__all__"


class RetailerTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetailerType
        fields = "__all__"


class ColourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colour
        fields = "__all__"


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = "__all__"
