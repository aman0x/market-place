from rest_framework import serializers
from subCategoryApp.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'

class SubCategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'