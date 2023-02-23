from rest_framework import serializers
from adsApp.models import Ads,Referral


class Referral(serializers.ModelSerializer):
    class Meta:
        model=Referral
        fields="__all__"


class AdsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Ads
        fields="__all__"


    