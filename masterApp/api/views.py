from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from masterApp.models import *



class UnitViewSet(viewsets.ModelViewSet):
     """
     API endpoint that allows groups to be viewed or edited.
     """
     queryset = Unit.objects.all().order_by('id')
     serializer_class = UnitSerializer
     permission_classes = [permissions.IsAuthenticated]
    #  lookup_field='state'

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

