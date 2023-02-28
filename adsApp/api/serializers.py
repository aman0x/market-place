from rest_framework import serializers
from adsApp.models import Ads,Referral


class ReferralSerializers(serializers.ModelSerializer):
    class Meta:
        model=Referral
        fields=["referred_by","commission","enter_percentage"]




class AdsSerializers(serializers.ModelSerializer):
    class Meta:
        model=Ads
        fields="__all__"
    