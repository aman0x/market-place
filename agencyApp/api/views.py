from rest_framework import viewsets
from rest_framework import permissions
from.serializers import AgencySerializers
from agencyApp.models import Agency



class AgencyViewset(viewsets.ModelViewSet):
    queryset=Agency.objects.all()
    serializer_class=AgencySerializers
    permission_classes=[permissions.IsAuthenticated]
