    
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from bazaarApp.models import Bazaar
from rest_framework import filters
from wholesellerApp.models import Wholeseller
from agentApp.models import Agent
from locationApp.models import State
from rest_framework.response import Response
from django.db.models import Count
from django.db import models


class BazarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']


    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.annotate(
            wholeseller_count=models.Count('wholeseller'),
            agent_count=models.Count('agent'),
            state_count=models.Count('bazaar_state')
        )
        return qs


class BazarAgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarAgentSerializer
    permission_classes = [permissions.IsAuthenticated]

class BazarWholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarWholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]    

class BazarProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    

class BazarViewReportTotalOrdersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportTotalOrdersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarViewReportTotalIncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportTotalIncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarViewReportCityWiseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportCityWiseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset
    
    def get_queryset(self):
        return Bazaar.objects.prefetch_related('bazaar_city', 'bazaar_product')

    def list_cities(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        cities = queryset.annotate(order_count=Count('bazaar_product')).values_list('bazaar_city__name', 'order_count')
        data = {}
        for city, order_count in cities:
            if city in data:
                data[city] += order_count
            else:
                data[city] = order_count
        return Response(data)


class BazarViewReportTopWholesellersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportTopWholesellersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarViewReportTopProductsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportTopProductsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset
    

class BazarViewReportNewWholesellersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarViewReportNewWholesellersSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarWholesellersListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarWholesellersListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarAgentsListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarAgentsListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset

class BazarProductsListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarProductsListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset
