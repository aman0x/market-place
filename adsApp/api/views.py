from rest_framework import viewsets
from .serializers import AdsSerializer,SlectStateSerializers,ReferralSerializers
from adsApp.models import Ads,Selectstate,Referral
from rest_framework import permissions

class AdsViewSets(viewsets.ModelViewSet):   
    queryset=Ads.objects.all()
    serializer_class=AdsSerializer
    permission_classes=[permissions.IsAuthenticated]


class StateViewSet(viewsets.ModelViewSet):
    queryset=Selectstate.objects.all()
    serializer_class=SlectStateSerializers

