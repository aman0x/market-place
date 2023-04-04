import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views ,status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import AgentSerializer,AgentManageCommisionSerializer,AgentCommisionRedeemSerializer
from agentApp.models import Agent,ManageCommision,AgentCommisionRedeem
from rest_framework import filters
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from wholesellerApp.models import Wholeseller
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


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
    
    

class AgentApplicationStatusViews(views.APIView):
    permission_classes=[permissions.AllowAny]


    def post(self, request):
       agent_number = request.data.get("agent_number")
       agent_status = request.data.get("agent_status")
       try:
            agent = Agent.objects.get(agent_number=agent_number)
            user = agent.agent_user
            if user is None:
                return Response({"message": "Agent user not found."})

            if agent_status == "CREATED":
                message = f"Your application_id {agent_number} is approved. If you have any Query? Fell free to contact Us ."
                return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            elif agent_status == "PENDING":
             message = f"Your application_id {agent_number} is In process./n we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
             return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            elif agent_status == "KYCREJECTED":
                     message = f"Your application_id {agent_number} is rejected ! Your pan image is very blurred and difficult to read. If you have any Query? Feel free to contact Us."
                     return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            else:
                return Response({"message": "Invalid agent status."})
       except Agent.DoesNotExist:
              return Response({"message": "Agent not found."})

class ReportPlanExpireView(views.APIView):
    
    def get(self, request):
        wholesalers = Wholeseller.objects.all()
        wholeseller_list = []
        for wholeseller in wholesalers:
              wholeseller_list.append(wholeseller.wholeseller_name)
        return Response(wholeseller_list, status=status.HTTP_200_OK)
    
    def post(self, request):
        wholeseller_name = request.data.get('wholeseller_name')
        
        try:
            wholeseller = Wholeseller.objects.get(wholeseller_name=wholeseller_name)
        except Wholeseller.DoesNotExist:
            return Response({'message': 'Wholeseller does not exist.'})
        
        days_left = (wholeseller.wholeseller_plan.end_date - datetime.now().date()).days
        
        if days_left <= 0:
            message = f"Your plan has expired. Please renew your plan."
            return Response({'message': message})
        elif days_left <= 15:
            message = f"Your plan will expire in {days_left} days."
            return Response({'message': message})
        elif days_left <= 30:
            message = f"Your plan will expire in {days_left} days. Please renew soon."
            return Response({'message': message})
        
        return Response({'message': 'Success'})
           

