from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import *
from retailerApp.models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import timedelta, datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
common_status = settings.COMMON_STATUS
import random
from rest_framework import filters


class RetailerViewSet(viewsets.ModelViewSet):
    serializer_class = RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["retailer_name"]

    def get_queryset(self):
        queryset = Retailer.objects.all()

        state_id = self.request.query_params.get('state_id')
        district_id = self.request.query_params.get('district_id')
        city_id = self.request.query_params.get('city_id')
        retailer_type = self.request.query_params.get('retailer_type_id')
        status = self.request.query_params.get('retailer_status')
        agent_type = self.request.query_params.get('retailer_agent_id')
        plan = self.request.query_params.get('plan')

        if state_id:
            queryset = queryset.filter(retailer_state_id=state_id)
        if district_id:
            queryset = queryset.filter(retailer_district_id=district_id)
        if city_id:
            queryset = queryset.filter(retailer_city_id=city_id)
        if retailer_type:
            queryset = queryset.filter(retailer_type_id=retailer_type)
        if status:
            queryset = queryset.filter(retailer_status__icontains=status)
        if agent_type:
            queryset = queryset.filter(retailer_agent_id=agent_type)
        if plan:
            queryset = queryset.filter(retailer_plan_id=plan)

        return queryset


class RetailerVerifyNumber(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        data = request.data
        retailer_number = data.get("retailer_number")
        password = data.get("retailer_otp")
        payload = {}
        if retailer_number != "":
            retailer_otp = random.randrange(000000, 999999)
            try:
                data = RetailerMobile.objects.get(retailer_number=retailer_number)
                data.retailer_otp = retailer_otp
                data.save(update_fields=["retailer_otp"])
                if data:
                    user = User.objects.filter(id=data.retailer_user_id).distinct().first()
                    if user:
                        payload = {
                            "otp": retailer_otp,
                            "details": "retailer OTP sent of registered mobile Number",
                        }
                        status_code = common_status["success"]["code"]
                    else:
                        payload = {"details": "No user found for the retailer"}
                        status_code = common_status["not_found"]["code"]
                else:
                    payload = {
                        "details": "No active account found with the given credentials"
                    }
                    status_code = common_status["not_found"]["code"]

            except Retailer.DoesNotExist:
                payload = {"details": "retailer not found"}
                status_code = common_status["unauthorized"]["code"]

        else:
            payload = {"details": "Something went wrong."}
            status_code = common_status["bad_request"]["code"]
            status_message = common_status["bad_request"]["message"]

        return Response(payload, status=status_code)

class RetailerVerifyOTP(views.APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        retailer_number = request.data.get("retailer_number")
        retailer_otp = request.data.get("retailer_otp")

        try:
            retailer = RetailerMobile.objects.get(retailer_number=retailer_number)
            if retailer.retailer_otp == int(retailer_otp):
                # OTP is valid
                retailer.retailer_otp = None
                retailer.save(update_fields=["retailer_otp"])
                # Get the User object associated with the retailer
                user = retailer.retailer_user
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
                        "retailer_id": retailer.id,
                    }
                )
            else:
                status_code = common_status["unauthorized"]["code"]
                payload = {"details": "Invalid OTP."}
                return Response(payload, status=status_code)
        except retailer.DoesNotExist:
            # retailer not found
            payload = {"details": "retailer not found"}
            status_code = common_status["unauthorized"]["code"]
            return Response(payload, status=status_code)


class AddToCart(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartSerializer
    queryset = SubCart.objects.all().order_by("id")

    def get_queryset(self):
        queryset = SubCart.objects.all().order_by("id")

        retailer_id = self.request.query_params.get('retailer_id')

        if retailer_id:
            queryset = queryset.filter(retailer_id=retailer_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save()

class Checkout(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CheckoutSerializer
    queryset = Cart.objects.all().order_by("id")

    def perform_create(self, serializer):
        serializer.save()

class WholesellerIdRetailerAPIView(views.APIView):
    serializer_class = WholesellerRetailerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id):
        retailers = Retailer.objects.filter(retailer_wholeseller=wholeseller_id)
        serializer = self.serializer_class(retailers, many=True)
        return Response(serializer.data)


class WholesellerIdRetailerIdViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, wholeseller_id, retailer_id):
        try:
            retailer = Retailer.objects.get(id=retailer_id, retailer_wholeseller__id=wholeseller_id)
            serializer = WholesellerRetailerSerializer(retailer)
            return Response(serializer.data)
        except Retailer.DoesNotExist:
            return Response(status=404)

# class RetailerNotification(viewsets.ModelViewSet):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RetailerSerializer
#
#     def get_queryset(self):
#         retailer_id = self.request.query_params.get("retailer_id")
#         queryset = Retailer.objects.all().order_by("id")
#         queryset = queryset.filter(id=retailer_id)
#
#         return queryset


class RetailerNumberViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetailerNumberSerializer
    queryset = RetailerMobile.objects.all().order_by("id")


class RetailerDetailsByNumberViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = RetailerSerializer

    def get_queryset(self):
        retailer_number = self.kwargs['retailer_number']
        retailer_number = '+' + str(retailer_number)
        queryset = Retailer.objects.filter(retailer_number__retailer_number=retailer_number)
        return queryset