from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from masterApp.models import *
from django_filters.rest_framework import DjangoFilterBackend



class UnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Unit.objects.all().order_by('id')
    serializer_class = UnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit_type']

class WholesellerTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = WholesellerType.objects.all().order_by('id')
    serializer_class = WholesellerTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class RetailerTypeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = RetailerType.objects.all().order_by('id')
    serializer_class = RetailerTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class ColourViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Colour.objects.all().order_by('id')
    serializer_class = ColourSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class SizeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Size.objects.all().order_by('id')
    serializer_class = SizeSerializer
    permission_classes = [permissions.IsAuthenticated]

