from rest_framework import viewsets
from rest_framework import permissions
from.serializers import *
from planApp.models import Plan
from rest_framework import filters
from rest_framework.response import Response

class PlanViewSet(viewsets.ModelViewSet):
    queryset=Plan.objects.all().order_by("id")
    filter_backends=[filters.SearchFilter]
    serializer_class=PlanSerializer
    permission_classes=[permissions.IsAuthenticated]
    search_fields=['plan_name']


class FeaturesViewSet(viewsets.ModelViewSet):
    queryset=PlanFeatures.objects.all().order_by("id")
    serializer_class=FeaturesSerializer
    permission_classes=[permissions.IsAuthenticated]

class RetailerPlanViewSet(viewsets.ModelViewSet):
    queryset=RetailerPlan.objects.all().order_by("id")
    filter_backends=[filters.SearchFilter]
    serializer_class=RetailerPlanSerializer
    permission_classes=[permissions.IsAuthenticated]
    search_fields=['plan_name']