from rest_framework import viewsets
from rest_framework import permissions
from categoryApp.models import Category
from .serializers import CategorySerializer


class CategoryAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
