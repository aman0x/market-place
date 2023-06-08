from rest_framework import serializers
from offerApp.models import Offers


# from parentCategoryApp.models import ParentCategory


class OfferSerializer(serializers.ModelSerializer):
    offer_name = serializers.SerializerMethodField()

    class Meta:
        model = Offers
        fields = '__all__'

    def get_offer_name(self, obj):
        try:
            name = obj.product.product_name
        except:
            name = "None"
        return name
