from rest_framework import viewsets
from rest_framework import permissions
from.serializers import *
from planApp.models import Plan
from rest_framework import filters
from rest_framework.response import Response

class PlanViewSet(viewsets.ModelViewSet):
    queryset=Plan.objects.all().order_by("id")
    filter_backends=[filters.SearchFilter]
    search_fields=['']
    permission_classes=[permissions.IsAuthenticated]
    

    # def get_queryset(self):
    #     plan_choice = self.request.query_params.get('free')
    #     if plan_choice:
    #         queryset = Plan.objects.filter(type=plan_choice).order_by('id')
    #     else:
    #         queryset = Plan.objects.all().order_by('id')
    #     return queryset
   

    def get_serializer_class(self):
        plan_type = self.request.query_params.get('type', None)
        if plan_type == 'free':
            return PlanFreeSerializer
        elif plan_type == 'paid':
            return PlanPaidSerializer
        return PlanPaidSerializer

class FeaturesProjectViewSet(viewsets.ModelViewSet):
    queryset=PlanFeaturesProject.objects.all().order_by("id")
    serializer_class=FeaturesProjectSerializer
    permission_classes=[permissions.IsAuthenticated]

class FeaturesSubscribersViewSet(viewsets.ModelViewSet):
    queryset=PlanFeaturesSubscribers.objects.all().order_by("id")
    serializer_class=FeaturesSubscribersSerializer
    permission_classes=[permissions.IsAuthenticated]