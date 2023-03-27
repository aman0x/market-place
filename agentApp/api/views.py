import random
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import AgentSerializer,AgentManageCommisionSerializer,AgentCommisionRedeemSerializer
from agentApp.models import Agent,ManageCommision,AgentCommisionRedeem
from rest_framework import filters
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User




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
