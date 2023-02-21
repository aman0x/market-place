from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, BazaarSerializer, BazaarAgentSerializer, BazaarWholesellerSerializer, BazaarProductSerializer
from bazaarApp.models import Bazaar
from rest_framework import filters




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class BazarViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['bazaar_name']

class BazarAgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarAgentSerializer
    permission_classes = [permissions.IsAuthenticated]

class BazarWholesellerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarWholesellerSerializer
    permission_classes = [permissions.IsAuthenticated]    

class BazarProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Bazaar.objects.all().order_by('id')
    serializer_class = BazaarProductSerializer
    permission_classes = [permissions.IsAuthenticated]


