from rest_framework import viewsets
from rest_framework import permissions
from .serializers import  BazaarReportSerializer, PlansSerializer, SummarySerializer
from bazaarApp.models import Bazaar





class SummaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = SummarySerializer
    permission_classes = [permissions.IsAuthenticated]
    

class BazaarReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    

class PlansViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = PlansSerializer
    permission_classes = [permissions.IsAuthenticated]
