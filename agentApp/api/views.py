from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AgentSerializer,AgentManageCommisionSerializer,AgentCommisionRedeemSerializer
from agentApp.models import Agent,ManageCommision,AgentCommisionRedeem
from rest_framework import filters

class AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_name']

class AgentCommisionViewset(viewsets.ModelViewSet):
    queryset=ManageCommision.objects.all()
    serializer_class=AgentManageCommisionSerializer
    permission_classes=[permissions.AllowAny]


class AgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset=AgentCommisionRedeem.objects.all()
    serializer_class=AgentCommisionRedeemSerializer
    permission_classes=[permissions.AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields=['id']
