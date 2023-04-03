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

common_status = {
    "success": {"code": 200, "message": "Request processed successfully"},
    "bad_request": {"code": 400, "message": "Bad request, please check your input data"},
    "unauthorized": {"code": 401, "message": "You are not authorized to perform this action"},
    "not_found": {"code": 404, "message": "The requested resource was not found"},
    "internal_server_error": {"code": 500, "message": "An internal server error occurred"},
}



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
    authentication_classes = []

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
                status_code = common_status["unauthorized"]["code"]
                payload = {
                    "details": "Invalid OTP."
                }
                return Response(payload, status=status_code)
        except Agent.DoesNotExist:
            # Agent not found
            payload = {
                "details": "Agent not found"
            }
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)

class AgentVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

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
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {
                            "details": "No user found for the agent"
                        }
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Agent.DoesNotExist:
                payload = {
                    "details": "Agent not found"
                }
                status_code = common_status["unauthorized"]["code"]


        else:
            payload = {
                "details": "Something went wrong."
            }
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]
            
        return Response(payload, status=status_code)
    
    

class AgentApplicationStatusView(views.APIView):
    def get(self, request, *args, **kwargs):
        application_id = kwargs.get('application_id')
        try:
            agent = Agent.objects.get(application_id=application_id)
        except Agent.DoesNotExist:
            return Response({'error': 'Agent not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if agent.agent_status == 'APPROVED':
            message = f'Your application ({application_id}) has been approved. For any further query please contact {agent.agent_number} or email {agent.agent_email}.'
        elif agent.agent_status == 'PENDING':
            message = f'Your application ({application_id}) is still pending. For any further query please contact {agent.agent_number} or email {agent.agent_email}.'
        else:
            message = f'Your application ({application_id}) has been rejected.'
        
        return Response({'message': message}, status=status.HTTP_200_OK)
