from rest_framework import viewsets
from rest_framework import permissions
from .serializer import PaymentSerializer
from paymentApp.models import Payment



class PaymentViewset(viewsets.ModelViewSet):
    queryset=Payment.objects.all().order_by('id')
    serializer_class=PaymentSerializer
    permission_classes=[permissions.IsAuthenticated]