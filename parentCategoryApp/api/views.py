from rest_framework import viewsets
from rest_framework import permissions
from parentCategoryApp.models import ParentCategory
from .serializers import ParentCategorySerializer
from rest_framework import filters


class ParentCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['parent_category_name']




