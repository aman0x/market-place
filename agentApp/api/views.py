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

class AgentVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        agent_number = data.get('agent_number')
        password = data.get('agent_otp')
        payload = {}
        if agent_number != '':
            agent_otp = random.randrange(1,  1000000)
            
            if agent_otp:
                data = Agent.objects.get(agent_number=agent_number)
                data.agent_otp= agent_otp
                data.save(update_fields = ['agent_otp'])
                if data != 0:
                    print(data)
                    user = User.objects.filter(id=data.agent_user_id
                    ).distinct()

                    refresh = Token.for_user(user)
                    payload = {"otp": agent_otp, 'refresh': str(refresh),
                               'access': str(refresh.access_token)}
                    
                else:
                    payload = {
                        "details": "No active account found with the given credentials"}
            else:
                data = "Something went wrong."
            
        return Response(payload)
