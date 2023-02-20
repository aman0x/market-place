from rest_framework import viewsets
from rest_framework import permissions
from .serializers import AgentSerializer
from agentApp.models import Agent
from rest_framework import filters

class AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_name']
