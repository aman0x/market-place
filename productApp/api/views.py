from rest_framework import viewsets
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

class FilterListAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = FilterListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product_subcategory','product_category','product_category_group']