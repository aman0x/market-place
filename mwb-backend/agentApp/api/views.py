import random
from datetime import timedelta, datetime
from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework import permissions
from .serializers import (
    AgentSerializer,
    AgentCommisionRedeemSerializer,
    WholsellerListSerializers,
    AgentWalletSerializer,
)
from agentApp.models import Agent, AgentCommisionRedeem
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from wholesellerApp.models import Wholeseller
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay
from django.db.models import Count, Sum
from django.conf import settings
from django.utils import timezone
from django.db import models
from datetime import date
from django.db.models.functions import ExtractYear, ExtractMonth, ExtractDay


common_status = settings.COMMON_STATUS
contact_number = settings.ADMIN_CONTACT_NUMBER
email = settings.ADMIN_EMAIL


class AgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["agent_name"]

    def get_queryset(self):
        queryset = Agent.objects.all().order_by("id")

        state_id = self.request.query_params.get('state_id')
        district_id = self.request.query_params.get('district_id')
        city_id = self.request.query_params.get('city_id')
        agent_type = self.request.query_params.get('agent_type')
        status = self.request.query_params.get('agent_status')
        active = self.request.query_params.get('active')

        if state_id:
            queryset = queryset.filter(agent_state_id=state_id)
        if district_id:
            queryset = queryset.filter(agent_district_id=district_id)
        if city_id:
            queryset = queryset.filter(agent_city_id=city_id)
        if status:
            queryset = queryset.filter(agent_status__icontains=status)
        if agent_type:
            queryset = queryset.filter(agent_type=agent_type)
        if active:
            queryset = queryset.filter(is_active=active)

        return queryset

class AgentCommisionRedeemViewset(viewsets.ModelViewSet):
    queryset = AgentCommisionRedeem.objects.all().order_by("id")
    serializer_class = AgentCommisionRedeemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["id"]


class AgentWallet(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def get(self, request, pk):
        data = {
            "total_amount_earned": 1000,
            "total_amount_withdrawn": 500,
            "agent_balance": 700,
            "agent_withdrawable_balance": 200,
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
                    return Response(
                        deserialized_data, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response("Agent is not valid")
        except:
            return Response("Agent is not available")


class AgentVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        agent_number = request.data.get("agent_number")
        agent_otp = request.data.get("agent_otp")

        try:
            agent = Agent.objects.get(agent_number=agent_number)
            if agent.agent_otp == int(agent_otp):
                # OTP is valid
                agent.agent_otp = None
                agent.save(update_fields=["agent_otp"])
                # Get the User object associated with the Agent
                user = agent.agent_user
                access_token = AccessToken.for_user(user)
                access_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=6400)
                )
                refresh_token = RefreshToken.for_user(user)
                refresh_token.set_exp(
                    from_time=datetime.utcnow(), lifetime=timedelta(seconds=166400)
                )
                return Response(
                    {
                        "access_token": str(access_token),
                        "refresh_token": str(refresh_token),
                        "agent_id": agent.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except Agent.DoesNotExist:
            # Agent not found
            payload = {"details": "Agent not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class AgentVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        agent_number = data.get("agent_number")
        password = data.get("agent_otp")
        payload = {}
        if agent_number != "":
            agent_otp = random.randrange(000000, 999999)
            try:
                data = Agent.objects.get(agent_number=agent_number)
                data.agent_otp = agent_otp
                data.save(update_fields=["agent_otp"])
                if data:
                    user = User.objects.filter(id=data.agent_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": agent_otp,
                            "details": "Agent OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the agent"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Agent.DoesNotExist:
                payload = {"details": "Agent not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)


class AgentApplicationStatusViews(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        agent_number = request.data.get("agent_number")
        agent_status = request.data.get("agent_status")
        kyc_remarks = request.data.get("kyc_remarks")
        try:
            agent = Agent.objects.get(agent_number=agent_number)
            user = agent.agent_user
            if user is None:
                return Response({"message": "Agent user not found."})

            if agent_status == "CREATED":
                message = f"Your application_id {agent_number} is in process. If you have any Query? Fell free to contact Us ."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "PENDING":
                message = f"Your application_id {agent_number} is in process. we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "KYCREJECTED" and kyc_remarks is not None:
                message = f"Your application_id {agent_number} is rejected ! {kyc_remarks}. If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            elif agent_status == "KYCAPPROVED":
                message = f"Your application_id {agent_number} is approved !  If you have any Query? Feel free to contact Us."
                return Response(
                    {
                        "message": message,
                        "contact_information": {
                            "email": email,
                            "phone_number": contact_number,
                        },
                    }
                )
            else:
                return Response({"message": "Invalid agent status."})
        except Agent.DoesNotExist:
            return Response({"message": "Agent not found."})


class ReportPlanExpireView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        base_url = request.build_absolute_uri('/')
        wholesalers = Wholeseller.objects.filter(wholeseller_agent_id=pk)
        wholeseller_list = []
        for wholeseller in wholesalers:
            today = datetime.now().date()
            try:
                end_date = wholeseller.wholeseller_plan.end_date
            except:
                end_date = None
            try:
                days_left = (end_date - today).days
            except:
                days_left = None
            try:
                wholeseller_image = str(wholeseller.wholeseller_image)
                if wholeseller_image:
                    wholeseller_image = base_url + wholeseller_image
                elif wholeseller_image == "":
                    wholeseller_image = "Image not found"
            except:
                wholeseller_image = "Image not found"
                
                
            status = "active"  # default value
            message = "Your plan is active."  # default value
            days = 0
            
            wholeseller_data = {
                "wholeseller_name": wholeseller.wholeseller_name,
                "wholeseller_image": wholeseller_image,
                "message": message,
                "status": status,
                "days": days,
            }

            if end_date == None:
                message = "No active plan! Please activate"
                status = "No Plan"
                days = "Not Applicable"

            elif days_left <= 0:
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

            wholeseller_data["message"] = message
            wholeseller_data["status"] = status
            wholeseller_data["days"] = days

            wholeseller_list.append(wholeseller_data)

        data = {"count": len(wholeseller_list), "wholesellers": wholeseller_list}
        return Response(data)


class WholesellerCountMonthView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
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

        month_names = settings.MONTH_NAMES

        monthly_counts = (
            qs.annotate(
                year=ExtractYear("created_at"), month=ExtractMonth("created_at")
            )
            .values("year", "month")
            .annotate(count=Count("id"))
        )

        monthly_result = []
        for item in monthly_counts:
            year_num = item["year"]
            month_num = item["month"]
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
            count = item["count"]
            monthly_result.append(
                {"year": year_num, "month": month_name, "count": count}
            )

        data = {
            "total_wholeseller_count": qs.count(),
            "wholesellers": monthly_result,
        }

        return Response(data)



class WholesellerCountView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get_week_number(self, year, month, day):
        date_obj = date(int(year), int(month), int(day))
        first_day = date_obj.replace(day=1)
        first_day_weekday = first_day.weekday()
        shift = (first_day_weekday + 1) % 7
        week_number = (date_obj.day + shift - 1) // 7 + 1
        return week_number

    def get_week_of_year(self, year, month, week_of_month):
        first_day_of_month = date(year, month, 1)
        first_week_of_month = first_day_of_month.isocalendar()[1]
        week_of_year = first_week_of_month + week_of_month - 1
        return week_of_year

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        week = request.query_params.get("week")
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
                year = int(year)
                month_num = int(month)
                week_of_month = int(week)
                week_of_year = self.get_week_of_year(year, month_num, week_of_month)
                qs = qs.filter(created_at__week=week_of_year)
            except ValueError:
                if year and month:
                    qs = qs.filter(created_at__year=year, created_at__month=month_num)
                else:
                    qs = qs.filter(created_at__year=year)

        month_names = settings.MONTH_NAMES

        yearly_counts = (
            qs.annotate(year=ExtractYear("created_at"))
            .values("year")
            .annotate(count=Count("id"))
        )

        monthly_counts = (
            qs.annotate(
                year=ExtractYear("created_at"), month=ExtractMonth("created_at")
            )
            .values("year", "month")
            .annotate(count=Count("id"))
        )

        week_counts = (
            qs.annotate(day=ExtractDay("created_at"), year=ExtractYear("created_at"), month=ExtractMonth("created_at"))
            .values("day", "year", "month")
            .annotate(count=Count("id"))
        )

        monthly_result = []
        for item in monthly_counts:
            year_num = item["year"]
            month_num = item["month"]
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
            count = item["count"]
            monthly_result.append(
                {"year": year_num, "month": month_name, "count": count}
            )

        week_result = []
        for item in week_counts:
            year_num = item["year"]
            month_num = item["month"]
            day_num = item["day"]
            week_num = self.get_week_number(year_num, month_num, day_num)
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
            week_name = "Week " + str(week_num)
            count = item["count"]

            existing_week = next((week for week in week_result if
                                  week["year"] == year_num and week["month"] == month_name and week[
                                      "week"] == week_name), None)

            if existing_week:
                # If the week already exists, increment the count
                existing_week["count"] += count
            else:
                # If the week does not exist, create a new entry
                week_result.append({"year": year_num, "month": month_name, "week": week_name, "count": count})

        data = {
            "total_wholeseller_count": qs.count(),
            "wholesellers": week_result,
        }

        return Response(data)

class WholesellerListViewset(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wholeseller.objects.all().order_by("id")
    serializer_class = WholsellerListSerializers
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["wholeseller_bazaar", "wholeseller_type"]

    def get_queryset(self):
        queryset = super().get_queryset()
        pk = self.kwargs.get("pk")
        if pk:
            queryset = queryset.filter(wholeseller_agent=pk)
        return queryset


class AgentEarningAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get_week_number(self, year, month, day):
        date_obj = date(int(year), int(month), int(day))
        first_day = date_obj.replace(day=1)
        first_day_weekday = first_day.weekday()
        shift = (first_day_weekday + 1) % 7
        week_number = (date_obj.day + shift - 1) // 7 + 1
        return week_number

    def get_week_of_year(self, year, month, week_of_month):
        first_day_of_month = date(year, month, 1)
        first_week_of_month = first_day_of_month.isocalendar()[1]
        week_of_year = first_week_of_month + week_of_month - 1
        return week_of_year

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        week = request.query_params.get("week")
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
                year = int(year)
                month_num = int(month)
                week_of_month = int(week)
                week_of_year = self.get_week_of_year(year, month_num, week_of_month)
                qs = qs.filter(created_at__week=week_of_year)
            except ValueError:
                if year and month:
                    qs = qs.filter(created_at__year=year, created_at__month=month_num)
                else:
                    qs = qs.filter(created_at__year=year)

        month_names = settings.MONTH_NAMES

        weekly_counts = (
            qs.annotate(year=ExtractYear("created_at"), month=ExtractMonth("created_at"), day=ExtractDay("created_at"))
            .values("year", "month", "day")
            .annotate(count=Count("id"), commission=Sum("wholeseller_plan__amount"))
        )

        total_commission = weekly_counts.aggregate(total_commission=Sum("commission"))["total_commission"]

        weekly_result = []
        for item in weekly_counts:
            year_num = item["year"]
            month_num = item["month"]
            day_num = item["day"]
            week_num = self.get_week_number(year_num, month_num, day_num)
            try:
                month_name = month_names[month_num]
            except KeyError:
                month_name = None
            week_name = "Week " + str(week_num)
            count = item["count"]
            commission = item["commission"]
            existing_week = next((week for week in weekly_result if
                                  week["year"] == year_num and week["month"] == month_name and week[
                                      "week"] == week_name), None)

            if existing_week:
                # If the week already exists, increment the count
                existing_week["count"] += count
            else:
                # If the week does not exist, create a new entry

                weekly_result.append({"year": year_num, "month": month_name, "week": week_name, "count": count, "commission": commission})

        data = {
            "TotalCommission": total_commission,
            "Earning": weekly_result,
        }

        return Response(data)

class AgentEarningMonthAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        year = request.query_params.get("year")
        month = request.query_params.get("month")
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

        month_names = settings.MONTH_NAMES

        monthly_counts = (
            qs.annotate(year=ExtractYear("created_at"), month=ExtractMonth("created_at"))
            .values("year", "month")
            .annotate(count=Count("id"), commission=Sum("wholeseller_plan__amount"))
        )

        total_commission = monthly_counts.aggregate(total_commission=Sum("commission"))["total_commission"]

        monthly_result = []
        for item in monthly_counts:
            year_num = item["year"]
            month_num = item["month"]
            try:
                month_name = month_names[month_num]
            except (KeyError, TypeError):
                month_name = None
            count = item["count"]
            commission = item["commission"]
            monthly_result.append(
                {"year": year_num, "month": month_name, "count": count, "commission": commission}
            )

        data = {
            "TotalCommission": total_commission,
            "Earning": monthly_result,
        }

        return Response(data)
