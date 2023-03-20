from rest_framework import viewsets,status, views
from rest_framework.response import Response
from rest_framework import permissions
from productApp.models import Product
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']

class ProductFilterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = FilterListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bazaar','category_group','category','subcategory']


class ProductUnitAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        payload = [{"unit_id": 1, "unit_value": "unit"}]
        return Response(payload)


class ProductWeightAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        payload = [{"weight_id": 1, "unit_value": "Kg"},
                   {"weight_id": 2, "unit_value": "Gram"}]
        return Response(payload)
