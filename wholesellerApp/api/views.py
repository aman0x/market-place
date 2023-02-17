from rest_framework import viewsets
from rest_framework import permissions
from .serializers import WholesellerSerializer
from wholesellerApp.models import Wholeseller
from rest_framework import filters


class WholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wholeseller_name']
