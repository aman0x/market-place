from rest_framework import serializers
from offerApp.models import Offers


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'

    def create(self, validated_data):
        return Offers.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass
