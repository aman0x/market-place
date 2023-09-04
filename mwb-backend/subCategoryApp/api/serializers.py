from rest_framework import serializers
from subCategoryApp.models import SubCategory
from drf_extra_fields.fields import Base64ImageField



class SubCategorySerializer(serializers.ModelSerializer):
    subcategory_ref_image = Base64ImageField(required=False)
    class Meta:
        model = SubCategory
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.subcategory_ref_image = validated_data.get(
            'subcategory_ref_image')
        event = super().update(instance, validated_data)
        return event

class SubCategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'