from rest_framework import viewsets
from rest_framework import permissions
from parentCategoryApp.models import ParentCategory
from .serializers import *
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class ParentCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['parent_category_name']

class ParentCategoryFilterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategoryFilterSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['bazaar']



