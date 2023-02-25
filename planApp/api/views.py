from rest_framework import viewsets
from rest_framework import permissions
from.serializers import *
from planApp.models import Plan,PlanFeatures
from rest_framework import filters
from rest_framework.response import Response

class PlanFreeViewSet(viewsets.ModelViewSet):
    queryset=Plan.objects.all().order_by("id")
    serializer_class=PlanFreeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['']
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        plan_type = self.request.query_params.get('type', None)
        if plan_type == 'free':
            queryset = Plan.objects.filter(plan_choice='FREE')
        elif plan_type == 'paid':
            queryset = Plan.objects.filter(plan_choice='PAID')
        else:
            queryset = self.queryset
        return queryset


    def update(self,request,*args,**kwargs):
        plan_object=self.get_object()
        data=request.data
        plan_choice=data.get('plan_choice',None)
        if plan_choice=='FREE':
                plan_object.plan_choice=Plan.FREE
                plan_object.save()
        elif plan_choice=='PAID':
                plan_object.plan_choice=Plan.PAID
                plan_object.save()
        serializer = self.get_serializer(plan_object, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
        