from rest_framework import serializers
from productApp.models import Product
from drf_extra_fields.fields import Base64ImageField

class ProductSerializer(serializers.ModelSerializer):
    product_upload_front_image = Base64ImageField(required=False)
    product_upload_back_image =  Base64ImageField(required=False)
    product_upload_mrp_label_image = Base64ImageField(required=False)

    class Meta:
        model = Product
        fields = '__all__'
    
    def update(self, instance, validated_data):
        instance.product_upload_front_image = validated_data.get(
            'product_upload_front_image')
        instance.product_upload_back_image = validated_data.get(
            'product_upload_back_image')
        instance.product_upload_mrp_label_image = validated_data.get(
            'product_upload_mrp_label_image')
        event = super().update(instance, validated_data)
        return event

class FilterListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

