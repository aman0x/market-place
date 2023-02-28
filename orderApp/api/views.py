from rest_framework import viewsets
from.serializers import OrderSerializer
from orderApp.models import Orders
from rest_framework import permissions


class OrderViewset(viewsets.ModelViewSet):
    queryset=Orders.objects.all()
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]
