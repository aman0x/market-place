import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views ,status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import AgentSerializer,AgentManageCommisionSerializer,AgentCommisionRedeemSerializer,WholsellerFilterSerializers
from agentApp.models import Agent,ManageCommision,AgentCommisionRedeem
from rest_framework import filters
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from wholesellerApp.models import Wholeseller
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.db.models import Count

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
    queryset = Agent.objects.all().order_by('id')
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['agent_name']


class AgentCommisionViewset(viewsets.ModelViewSet):
    queryset=ManageCommision.objects.all().order_by('id')
    serializer_class=AgentManageCommisionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset=AgentCommisionRedeem.objects.all().order_by('id')
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
                message = f"Your application_id {agent_number} is in process./n If you have any Query? Fell free to contact Us ."
                return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            elif agent_status == "PENDING":
             message = f"Your application_id {agent_number} is in process./n we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
             return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            elif agent_status == "KYCREJECTED":
                     message = f"Your application_id {agent_number} is rejected ! Your pan image is very blurred and difficult to read. If you have any Query? Feel free to contact Us."
                     return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            elif agent_status == "KYCAPPROVED":
                     message = f"Your application_id {agent_number} is approved !  If you have any Query? Feel free to contact Us."
                     return Response({"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
            else:
                return Response({"message": "Invalid agent status."})
       except Agent.DoesNotExist:
              return Response({"message": "Agent not found."})

class ReportPlanExpireView(views.APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request):
        wholesellers = Wholeseller.objects.all()
        wholeseller_list = []
        for wholeseller in wholesellers:
              wholeseller_list.append(wholeseller.wholeseller_name)
        return Response(wholeseller_list, status=status.HTTP_200_OK)
    @csrf_exempt
    def post(self, request):
        today = datetime.now().date()
        wholeseller_name = request.data.get('wholeseller_name')
        try:
            wholeseller = Wholeseller.objects.get(wholeseller_name=wholeseller_name)
        except Wholeseller.DoesNotExist:
            return Response({'message': 'Wholeseller does not exist.'})
        end_date = wholeseller.wholeseller_plan.end_date
        days_left = (today - end_date).days
  
        if days_left <= 0:
            message = f"{wholeseller_name} your plan has expired.{days_left} .Please renew your plan."
            return Response({'message': message})
        elif days_left <= 15:
            return Response({'message': message})
        elif days_left <= 30:
            message = f"{wholeseller_name} your plan will expire in {days_left} days. Please renew soon."
            return Response({'message': message})

        return Response({'message': 'Success'})
           


class WholesellerCountView(views.APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request):
        year = request.query_params.get('year')
        month = request.query_params.get('month')

        qs = Wholeseller.objects.all()
        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            qs = qs.filter(created_at__month=month)
        
        month_names = {
            1: 'January',
            2: 'February',
            3: 'March',
            4: 'April',
            5: 'May',
            6: 'June',
            7: 'July',
            8: 'August',
            9: 'September',
            10: 'October',
            11: 'November',
            12: 'December'
        }
        
        yearly_counts = qs.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id'))
        yearly_result = []
        for item in yearly_counts:
            year_num = item['year']
            count = item['count']
            yearly_result.append({'year': year_num, 'count': count})

        monthly_counts = qs.annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at')).values('year', 'month').annotate(count=Count('id'))
        monthly_result = []
        for item in monthly_counts:
            year_num = item['year']
            month_num = item['month']
            month_name = month_names.get(month_num)
            count = item['count']
            monthly_result.append({'year': year_num, 'month': month_name, 'count': count})

        week_counts = qs.annotate(week=ExtractWeek('created_at')).values('week').annotate(count=Count('id'))
        week_result = []
        for item in week_counts:
            week_num = item['week']
            week_name = 'Week ' + str(week_num)
            count = item['count']
            week_result.append({'week': week_name, 'count': count})


        data = {
            'total_wholeseller_count': qs.count(),
            'no of wholeseller by year': yearly_result,
            'no of wholeseller by months': monthly_result,
            'no of wholeseller by week': week_result

        } 

        return Response(data)


class WholesellerFilterViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Agent.objects.all().order_by('id')
    serializer_class = WholsellerFilterSerializers
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['wholeseller_type','wholeseller_bazaar']

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(pk=pk)
        return queryset
