import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import AgentSerializer, AgentManageCommisionSerializer, AgentCommisionRedeemSerializer, WholsellerListSerializers, AgentWalletSerializer
from agentApp.models import Agent, ManageCommision, AgentCommisionRedeem
from rest_framework import filters
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from wholesellerApp.models import Wholeseller
from django_filters.rest_framework import DjangoFilterBackend
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractWeek
from django.db.models import Count
from datetime import date, timedelta
from django.conf import settings
from django.utils import timezone
from django.db import models


common_status = settings.COMMON_STATUS



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
    queryset = ManageCommision.objects.all().order_by('id')
    serializer_class = AgentManageCommisionSerializer
    permission_classes = [permissions.IsAuthenticated]


class AgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset = AgentCommisionRedeem.objects.all().order_by('id')
    serializer_class = AgentCommisionRedeemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']


class AgentWallet(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, pk):
        data = {
            'total_amount_earned': 1000,
            'total_amount_withdrawn': 500,
            'agent_balance': 700,
            'agent_withdrawable_balance': 200,
        }
        serializer = AgentWalletSerializer(data=data)
        deserialized_data = ""
        try:
            agent = Agent.objects.get(id=pk)
            if agent:
                if serializer.is_valid():
                    deserialized_data = serializer.validated_data
                    return Response(deserialized_data, status=status.HTTP_200_OK)
                else:
                    return Response(deserialized_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Agent is not valid")
        except:
            return Response("Agent is not available")


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
                    "refresh_token": str(refresh_token),
                    "user_id": user.id
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
            agent_otp = random.randrange(000000, 999999)
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
    permission_classes = [permissions.AllowAny]

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
                return Response(
                    {"message": message, "contact_information": {"email": user.email, "phone_number": '+91123456789'}})
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
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        wholesalers = Wholeseller.objects.filter(wholeseller_agent_id=pk)
        wholeseller_list = []
        for wholeseller in wholesalers:
            today = datetime.now().date()
            end_date = wholeseller.wholeseller_plan.end_date
            days_left = (end_date - today).days

            status = "active"  # default value
            message = "Your plan is active."  # default value
            days = 0

            wholeseller_data = {
                'wholeseller_name': wholeseller.wholeseller_name,
                'message': message,
                'status': status,
                'days': days
            }

            if days_left <= 0:
                message = "Your plan has expired. Please renew your plan."
                status = "expired"
                days = f"expired by {abs(days_left)} days"

            elif days_left <= 15:
                message = f"Your plan will expiring soon. Please renew soon."
                status = "expiring_soon"
                days = f"expiring in {abs(days_left)} days"
            elif days_left <= 30:
                message = f"Your plan will expire . Please renew soon."
                status = "expiring_soon"
                days = f"expiring in {abs(days_left)} days"

            wholeseller_data['message'] = message
            wholeseller_data['status'] = status
            wholeseller_data['days'] = days

            wholeseller_list.append(wholeseller_data)

        data = {
            'count': len(wholeseller_list),
            'wholesellers': wholeseller_list
        }
        return Response(data)


class WholesellerCountView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        week = request.query_params.get('week')
        wholeseller_agent = pk

        qs = Wholeseller.objects.filter(wholeseller_agent=wholeseller_agent)

        if year:
            qs = qs.filter(created_at__year=year)
        if month:
            try:
                month_num = int(month)
                qs = qs.filter(created_at__month=month_num)
            except ValueError:
                qs = qs.filter(created_at__year=year)
        if week:
            try:
                week_num = int(week)
                qs = qs.filter(created_at__week=week_num)
            except ValueError:
                if year and month:
                    qs = qs.filter(created_at__year=year, created_at__month=month_num)
                else:
                    qs = qs.filter(created_at__year=year)

        month_names = settings.MONTH_NAMES
        yearly_counts = qs.annotate(year=ExtractYear('created_at')).values('year').annotate(count=Count('id'))
        yearly_result = []
        for item in yearly_counts:
            year_num = item['year']
            count = item['count']
            yearly_result.append({'year': year_num, 'count': count})

        monthly_counts = qs.annotate(year=ExtractYear('created_at'), month=ExtractMonth('created_at')).values('year',
                                                                                                              'month').annotate(
            count=Count('id'))
        monthly_result = []
        for item in monthly_counts:
            year_num = item['year']
            month_num = item['month']
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
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


class WholesellerListViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wholeseller.objects.all().order_by('id')
    serializer_class = WholsellerListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["wholeseller_bazaar","wholeseller_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get('pk')
        if pk:
            queryset=queryset.filter(wholeseller_agent=pk)
        return queryset


class AgentEarningAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        week = request.query_params.get('week')

        try:
            total_wholesellers_added = Wholeseller.objects.filter(wholeseller_agent=pk)

            # Filter by year
            if year:
                total_wholesellers_added = total_wholesellers_added.filter(created_at__year=year)

            # Filter by month
            if month:
                total_wholesellers_added = total_wholesellers_added.filter(created_at__month=month)

            # Filter by week
            if week:
                start_date = timezone.now().date() - timedelta(weeks=52)  # consider only past 52 weeks
                total_wholesellers_added = total_wholesellers_added.filter(
                    created_at__range=[start_date, timezone.now().date()]).annotate(
                    week_num=Count('id', filter=(models.Q(created_at__week=week))))

            count = total_wholesellers_added.count()
            if count > 0:
                total_commission = 0
                for wholeseller in total_wholesellers_added:
                    if wholeseller.wholeseller_plan:
                        total_commission += wholeseller.wholeseller_plan.amount

                response_data = {
                    "total_wholesellers_added": count,
                    "total_commission": total_commission
                }

            else:
                response_data = {
                    "message": "No data available for this agent."
                }

        except Agent.DoesNotExist:
            response_data = {
                "message": "No data available for this agent."
            }

        return Response(response_data)
