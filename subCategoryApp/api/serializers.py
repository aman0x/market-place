from rest_framework import serializers
from subCategoryApp.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'subcategory_name')
