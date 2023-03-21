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
    search_fields=['firm_name']
    

    # def get_queryset(self):
    #     plan_choice = self.request.query_params.get('free')
    #     if plan_choice:
    #         queryset = Plan.objects.filter(type=plan_choice).order_by('id')
    #     else:
    #         queryset = Plan.objects.all().order_by('id')
    #     return queryset
   

    # def get_serializer_class(self):
    #     plan_type = self.request.query_params.get('type', None)
    #     if plan_type == 'free':
    #         return PlanFreeSerializer
    #     elif plan_type == 'paid':
    #         return PlanPaidSerializer
    #     return PlanPaidSerializer

class FeaturesViewSet(viewsets.ModelViewSet):
    queryset=PlanFeatures.objects.all().order_by("id")
    serializer_class=FeaturesSerializer
    permission_classes=[permissions.IsAuthenticated]