from rest_framework import serializers
from categoryApp.models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
