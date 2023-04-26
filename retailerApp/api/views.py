from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from retailerApp.models import Retailer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import requests
import json


class RetailerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['retailer_name']

