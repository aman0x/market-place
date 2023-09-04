from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import *
from bazaarApp.models import Bazaar
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from wholesellerApp.models import Wholeseller
from agentApp.models import Agent
from django.db.models import Sum,Count
from planApp.models import Plan
from decimal import Decimal
# from planApp.models import PlanFeaturesSubscribers
from django.db import models


class SummaryViewSet(views.APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, format=None):
        # Query the database to get the summary data
        #bazaar_count = Wholeseller.objects.values('wholeseller_bazaar').distinct().count()
        bazaar_count=Bazaar.objects.count()
        wholeseller_count = Wholeseller.objects.count()
        agent_count=Agent.objects.count()
        #revenue_sum = Wholeseller.objects.aggregate(revenue_sum=Sum('revenue'))['revenue_sum']
        #bill_sum = Wholeseller.objects.aggregate(bill_sum=Sum('bill'))['bill_sum']
        ##agent_count = Wholeseller.objects.values('wholeseller_agent').distinct().count()
        #commission_sum = Wholeseller.objects.aggregate(commission_sum=Sum('commission'))['commission_sum']
        #customer_count = Wholeseller.objects.values('customer').distinct().count()
        
        # Create a dictionary with the summary data
        summary_data = {
            'bazaar': bazaar_count,
            'wholeseller': wholeseller_count,
            'agent':agent_count,
            #'revenue': revenue_sum,
            #'bill': bill_sum,
            #'agent': agent_count,
            #'commission': commission_sum,
            #'customer': customer_count,
        }
        
        serializer = SummarySerializer(summary_data)
        
        return Response(serializer.data)

class BazaarReportViewSet(views.APIView):
    permission_classes=[permissions.IsAuthenticated]


    def get(self, request):
        data = {}
        data['wholeseller'] = Wholeseller.objects.count()
        data['agent'] = Agent.objects.count()
        #data['bill'] = Order.objects.count()
        #data['revenue'] = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        #data['commission'] = Order.objects.aggregate(Sum('commission'))['commission__sum'] or 0
        #data['customer'] = Order.objects.aggregate(Count('customer', distinct=True))['customer__count'] or 0
        serializer= BazaarReportSerializer(data)
        return Response(serializer.data)


class PlansViewSet(views.APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        plans_count = Plan.objects.count()
        # subscribers_count = PlanFeaturesSubscribers.objects.values('plan').annotate(count=Count('subscribers')).count()
        #revenue_sum = PlanFeaturesSubscribers.objects.aggregate(sum=Sum('amount'))['sum'] or 0
        
        data = {
            'plan': plans_count,
            # 'subscriber': subscribers_count,
            #'revenue': revenue_sum
        }
        
        serializer = PlansSerializer(data)
        return Response(serializer.data) 


         

class PlanListViewSet(viewsets.ModelViewSet):
     queryset = Plan.objects.all()
     serializer_class = PlanListSerializer

     def get_queryset(self):
         queryset = super().get_queryset()
         plan_choice = self.request.query_params.get('plan_choice', None)
         city = self.request.query_params.get('city', None)
         state = self.request.query_params.get('state', None)
         bazaar = self.request.query_params.get('bazaar', None)

         if plan_choice is not None:
             queryset = queryset.filter(plan_choice__icontains=plan_choice)
         if city is not None:
             queryset = queryset.filter(city__name__icontains=city)
         if state is not None:
             queryset = queryset.filter(state__name__icontains=state)
         if bazaar is not None:
             queryset = queryset.filter(bazaar__name__icontains=bazaar)

         return queryset

# class PlanListViewSet(viewsets.ModelViewSet):
# #     """
# #     API endpoint that allows groups to be viewed or edited.
# #     # """
#      queryset = Bazaar.objects.all().order_by('id')
#      serializer_class = PlanListSerializer
#      permission_classes = [permissions.IsAuthenticated]
#      filter_backends = [DjangoFilterBackend]
#      filterset_fields = ['bazaar_name', 'bazaar_state', 'bazaar_district']

    
class BazaarListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    # """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarListSerializer
    permission_classes = [permissions.IsAuthenticated]
