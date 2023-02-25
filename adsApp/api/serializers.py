from rest_framework import serializers
from adsApp.models import Ads,Referral,Selectstate


class ReferralSerializers(serializers.ModelSerializer):
    class Meta:
        model=Referral
        fields="__all__"


class SlectStateSerializers(serializers.ModelSerializer):
    class Meta:
        model=Selectstate
        fields=("state_name","city_name")

class AdsSerializer(serializers.ModelSerializer):
    slect_state=SlectStateSerializers()
    class Meta:
        model=Ads
        fields="__all__"


    def create(self, validated_data):
        slect_state = validated_data.pop('slect_state')
        ads = Ads.objects.create(**validated_data)
        for slect_state in slect_state:
            state, created = Selectstate.objects.get_or_create(**slect_state)
            ads.select_state.add(state)
        return ads

    def update(self,validated_data,instance):
        slect_state=validated_data.pop('slect_state')
        instance.state=validated_data.get('title',instance.state)
        instance.save()
        for slect_state in slect_state:
            state,created=Selectstate.objects.get_or_create(**slect_state)
            instance.state.add(state)
            return instance
