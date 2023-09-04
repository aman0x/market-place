from rest_framework import serializers
from categoryApp.models import Category
from drf_extra_fields.fields import Base64ImageField



class CategorySerializer(serializers.ModelSerializer):
    category_ref_image = Base64ImageField(required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.category_ref_image = validated_data.get('category_ref_image')
        event = super().update(instance, validated_data)
        return event

class CategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
