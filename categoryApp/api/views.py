from rest_framework import viewsets
from rest_framework import permissions
from categoryApp.models import Category
from .serializers import CategorySerializer
from rest_framework import filters


class CategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['category_name']
