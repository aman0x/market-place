from rest_framework import serializers
from parentCategoryApp.models import ParentCategory


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'
