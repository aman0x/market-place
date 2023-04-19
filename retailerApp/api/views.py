from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from wholesellerApp.models import Wholeseller
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import requests
import json


class WholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializerAll
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wholeseller_name']


class WholesellerDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wholeseller_type']



class WholesellerDashboardBazzarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = Wholeseller_bazzarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wholeseller_type']

    # def list(self, request, *args, **kwargs):
    #     response = requests.get('http://127.0.0.1:8000/api/product/filter/')
    #     data = response.json()
    #     print(data) # Print the data to the console
    #     # Call the super class's list method to return the default response
    #     result = super().list(request, *args, **kwargs)
    #     return  result