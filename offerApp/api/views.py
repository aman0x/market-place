from offerApp.models import Offers
from .serializers import *
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all().order_by('id')
    serializer_class = OfferSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["offer_coupon_code"]
