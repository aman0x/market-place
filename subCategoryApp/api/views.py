from rest_framework import viewsets
from rest_framework import permissions
from subCategoryApp.models import SubCategory
from .serializers import SubCategorySerializer
from rest_framework import filters


class SubCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['subcategory_name']    

