from rest_framework import viewsets, views
from rest_framework import permissions
from .serializers import *
from retailerApp.models import Retailer
from rest_framework import filters
import random
from django.contrib.auth.models import User
from rest_framework.response import Response
from datetime import timedelta, datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings
common_status = settings.COMMON_STATUS


class RetailerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Retailer.objects.all()
    serializer_class = RetailerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['retailer_name']

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
                data = Retailer.objects.get(retailer_number=retailer_number)
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
            retailer = Retailer.objects.get(retailer_number=retailer_number)
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
