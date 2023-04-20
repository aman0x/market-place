from rest_framework import viewsets, views, status
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
from wholesellerApp.models import Wholeseller
from productApp.models import Product
from django.contrib.auth.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import requests
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.db.models import Q

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


class WholesellerProductViewSet(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    # serializer_class = WholesellerProductSerializer
    # lookup_field = 'id'

    def get(self, request, pk):
        category = request.query_params.get('category')
        subcategory = request.query_params.get('subcategory')
        wholeseller_queryset = Wholeseller.objects.filter(id=pk)
        data = wholeseller_queryset.all().values_list("wholeseller_bazaar")
        product_ids = []
        payload = []
        count = 0
        for bazaar_id in data:
            Product_queryset = Product.objects.filter(bazaar=bazaar_id)
            for product in Product_queryset:
                id = product.id
                product_ids.append(id)

        for id in product_ids:
            if category != '' and subcategory == '':
                product = Product.objects.filter(Q(id=id) & Q(category_id=category))
            elif subcategory != '' and category == '':
                product = Product.objects.filter(Q(id=id) & Q(subcategory_id=subcategory))
            elif subcategory is None and category is None:
                product = Product.objects.filter(id=id)
            elif subcategory != '' and category != '':
                product = Product.objects.filter(Q(id=id) & Q(subcategory_id=subcategory) & Q(category_id=category))
            elif subcategory == "" and category == "":
                product = Product.objects.filter(id=id)

            Product_data = product.all().values()
            for Product_data in Product_data:
                payload.append(Product_data)
                count += 1

        return Response({"count": count, "result": payload})


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
                return Response(
                    {"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            elif wholeseller_status == "KYCREJECTED":
                message = f"Your application_id {wholeseller_number} is rejected ! Your pan image is very blurred and difficult to read. If you have any Query? Feel free to contact Us."
                return Response(
                    {"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            elif wholeseller_status == "KYCAPPROVED":
                message = f"Your application_id {wholeseller_number} is approved !  If you have any Query? Feel free to contact Us."
                return Response(
                    {"message": message, "contact_information": {"email": user.email, "phone_number": contact_number}})
            else:
                return Response({"message": "Invalid agent status."})
        except Wholeseller.DoesNotExist:
            return Response({"message": "Wholeseller not found."})
