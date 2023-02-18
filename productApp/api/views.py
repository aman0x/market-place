from rest_framework import viewsets
from rest_framework import permissions
from productApp.models import Product
from rest_framework import filters
from .serializers import ProductSerializer


class ProductAPIView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['product_name']
