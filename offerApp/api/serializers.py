from rest_framework import serializers
from offerApp.models import Offers
from drf_extra_fields.fields import Base64ImageField

# from parentCategoryApp.models import ParentCategory


class OfferSerializer(serializers.ModelSerializer):
    offer_name = serializers.SerializerMethodField()
    offer_image = Base64ImageField(required=False)

    class Meta:
        model = Offers
        fields = '__all__'

    def get_offer_name(self, obj):
        try:
            name = obj.product.product_name
        except:
            name = "None"
        return name

    def update(self, instance, validated_data):
        instance.offer_image = validated_data.get('offer_image')
        event = super().update(instance, validated_data)
        return event