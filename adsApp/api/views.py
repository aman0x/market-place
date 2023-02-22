from rest_framework import viewsets
from .serializers import AdsSerializer
from adsApp.models import Ads
from rest_framework import permissions

class AdsViewsets(viewsets.ModelViewSet):
    queryset=Ads.objects.all()
    serializer_class=AdsSerializer
    permission_classes=[permissions.IsAuthenticated]