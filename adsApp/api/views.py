from rest_framework import viewsets
from .serializers import AdsSerializers,ReferralSerializers
from adsApp.models import Referral,Ads
from rest_framework import permissions


class AdsViewset(viewsets.ModelViewSet):
    queryset=Ads.objects.all().order_by("id")
    serializer_class=AdsSerializers
    permission_classes=[permissions.IsAuthenticated]



class ReferralViewsets(viewsets.ModelViewSet):
    queryset=Referral.objects.all().order_by("id")
    serializer_class=ReferralSerializers
    permission_classes=[permissions.IsAuthenticated]
