<<<<<<< Updated upstream
from rest_framework import viewsets, views, status
=======
from rest_framework import viewsets, views
>>>>>>> Stashed changes
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from wholesellerApp.models import Wholeseller
from django.contrib.auth.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import requests
import json
<<<<<<< Updated upstream
from django.conf import settings
from rest_framework.response import Response
=======

class WholesalerLogin(views.APIView):
    permission_classes = []
    def get(self, request, format=None):
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)
    
>>>>>>> Stashed changes

class WholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializerAll
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['wholeseller_name']


class WholesellerDashboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = WholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wholeseller_type']



class WholesellerDashboardBazzarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Wholeseller.objects.all()
    serializer_class = Wholeseller_bazzarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['wholeseller_type']


class WholesellerApplicationStatusViews(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        wholeseller_number = request.data.get("wholeseller_number")
        wholeseller_status = request.data.get("wholeseller_status")
        contact_number = settings.CONTACT_NUMBER
        try:
            wholeseller = Wholeseller.objects.get(wholeseller_number=wholeseller_number)
            user = wholeseller.wholeseller_user
            if user is None:
                return Response({"message": "Wholeseller user not found."})

            if wholeseller_status == "CREATED":
                message = f"Your application_id {wholeseller_number} is in process./n If you have any Query? Fell free to contact Us ."
                return Response(
                    {"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            elif wholeseller_status == "PENDING":
                message = f"Your application_id {wholeseller_number} is in process./n we have received your Application, Our team is reviewing it. Thank You for your patience .if you have any Query? Fell free to contact Us."
                return Response({"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            elif wholeseller_status == "KYCREJECTED":
                message = f"Your application_id {wholeseller_number} is rejected ! Your pan image is very blurred and difficult to read. If you have any Query? Feel free to contact Us."
                return Response({"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            elif wholeseller_status == "KYCAPPROVED":
                message = f"Your application_id {wholeseller_number} is approved !  If you have any Query? Feel free to contact Us."
                return Response({"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            else:
                return Response({"message": "Invalid agent status."})
        except Wholeseller.DoesNotExist:
            return Response({"message": "Wholeseller not found."})