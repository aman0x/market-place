from rest_framework import viewsets
from rest_framework import permissions
from categoryApp.models import Category
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_name']

class CategoryFilterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategoryFilterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bazaar','category_group']