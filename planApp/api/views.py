from rest_framework import viewsets
from rest_framework import permissions
from.serializers import PlanSerializers,PlanFeatureSerializers
from planApp.models import Plan,PlanFeatures
from rest_framework import filters

class PlanFreeViewSet(viewsets.ModelViewSet):
    queryset=Plan.objects.all().order_by("id")
    serializer_class=PlanSerializers
    filter_backends=[filters.SearchFilter]
    search_fields=['']
    permission_classes=[permissions.IsAuthenticated]

