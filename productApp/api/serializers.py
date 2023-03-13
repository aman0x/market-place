from rest_framework import serializers
from productApp.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class FilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'