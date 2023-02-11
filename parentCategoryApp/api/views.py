from rest_framework import viewsets
from rest_framework import permissions
from parentCategoryApp.models import ParentCategory
from .serializers import ParentCategorySerializer


class ParentCategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ParentCategory.objects.all()
    serializer_class = ParentCategorySerializer





