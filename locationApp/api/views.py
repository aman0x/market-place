from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from locationApp.models import *



class StateViewSet(viewsets.ModelViewSet):
     """
     API endpoint that allows groups to be viewed or edited.
     """
     queryset = State.objects.all().order_by('id')
     serializer_class = StateSerializer
     permission_classes = [permissions.IsAuthenticated]
     lookup_field='state'

class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = District.objects.all().order_by('id')
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]




