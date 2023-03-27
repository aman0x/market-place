from rest_framework import serializers
from parentCategoryApp.models import ParentCategory
from drf_extra_fields.fields import Base64ImageField


class ParentCategorySerializer(serializers.ModelSerializer):
    parent_category_ref_image = Base64ImageField(required=False)
    class Meta:
        model = ParentCategory
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.parent_category_ref_image = validated_data.get(
            'parent_category_ref_image')
        event = super().update(instance, validated_data)
        return event

class ParentCategoryFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParentCategory
        fields = '__all__'