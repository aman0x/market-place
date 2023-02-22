
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import BazaarSerializer, BazaarAgentSerializer, BazaarWholesellerSerializer, BazaarProductSerializer
from bazaarApp.models import Bazaar
from rest_framework import filters






class BazarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']

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


