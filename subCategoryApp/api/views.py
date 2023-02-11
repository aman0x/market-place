from rest_framework import viewsets
from rest_framework import permissions
from subCategoryApp.models import SubCategory

from .serializers import SubCategorySerializer


class SubCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
