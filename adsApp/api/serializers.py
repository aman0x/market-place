from rest_framework import serializers
from adsApp.models import Ads


class AdsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Ads
        fields="__all__"