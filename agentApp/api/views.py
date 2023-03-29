import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import AgentSerializer,AgentManageCommisionSerializer,AgentCommisionRedeemSerializer,ApplicationStatusSerializer
from agentApp.models import Agent,ManageCommision,AgentCommisionRedeem
from rest_framework import filters
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status





class AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_name']


class AgentCommisionViewset(viewsets.ModelViewSet):
    queryset=ManageCommision.objects.all()
    serializer_class=AgentManageCommisionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset=AgentCommisionRedeem.objects.all()
    serializer_class=AgentCommisionRedeemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields=['id']


class AgentVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        agent_number = request.data.get('agent_number')
        agent_otp = request.data.get('agent_otp')

        try:
            agent = Agent.objects.get(agent_number=agent_number)
            if agent.agent_otp == int(agent_otp):
                # OTP is valid
                agent.agent_otp = None
                agent.save(update_fields=['agent_otp'])
                # Get the User object associated with the Agent
                user = agent.agent_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400))
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400))
                

                return Response({
                    "access_token": str(access_token),
                    "refresh_token": str(refresh_token)
                })
            else:
                # Invalid OTP
                return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except Agent.DoesNotExist:
            # Agent not found
            return Response({"detail": "Agent not found."}, status=status.HTTP_404_NOT_FOUND)

class AgentVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        data = request.data
        agent_number = data.get('agent_number')
        password = data.get('agent_otp')
        payload = {}
        if agent_number != '':
            agent_otp = random.randrange(1,  1000000)
            try:
                data = Agent.objects.get(agent_number=agent_number)
                data.agent_otp = agent_otp
                data.save(update_fields=['agent_otp'])
                if data:
                    user = User.objects.filter(
                        id=data.agent_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": agent_otp,
                            "details": "Agent OTP sent of registered mobile Number"
                        }
                    else:
                        payload = {
                            "details": "No user found for the agent"
                        }
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
            except Agent.DoesNotExist:
                payload = {
                    "details": "Agent not found"
                }


        else:
            payload = {
                "details": "Something went wrong."
            }
            
        return Response(payload)
    
    

