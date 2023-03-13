from rest_framework import viewsets
from rest_framework import permissions
from subCategoryApp.models import SubCategory
from .serializers import SubCategorySerializer
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class SubCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['subcategory_name']    

class SubCategoryFilterAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
