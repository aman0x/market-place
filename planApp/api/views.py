from rest_framework import viewsets
from rest_framework import permissions
from.serializers import AddPlanSerializers,PlanPaidSerializers,PlanSerializers
from planApp.models import PlanPaid,AddPlan,Plan
from rest_framework import filters

class Planviewset(viewsets.ModelViewSet):
    queryset=Plan.objects.all().order_by("id")
    serializer_class=PlanSerializers
    filter_backends=[filters.SearchFilter]
    search_fields=['']
    permission_classes=[permissions.IsAuthenticated]


#class AddplanViewset(viewsets.ModelViewSet):
 #   queryset=AddPlan.objects.all().order_by("id")    
  #  serializer_class=PlanSerializers
   # permission_classes=[permissions.IsAuthenticated]

#class planPaidViewset(viewsets.ModelViewSet):
 #   queryset=PlanPaid.objects.all().order_by("id")
  #  serializer_class=PlanSerializers
   # permission_classes=[permissions.IsAuthenticated]    


