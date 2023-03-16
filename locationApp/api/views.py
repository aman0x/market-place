from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *
from locationApp.models import *



class StateViewSet(viewsets.ModelViewSet):
     """
     API endpoint that allows groups to be viewed or edited.
     """
     queryset = State.objects.all().order_by('id')
     serializer_class = StateSerializer
     permission_classes = [permissions.IsAuthenticated]
    #  lookup_field='state'

class CityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer
    permission_classes = [permissions.IsAuthenticated]

class DistrictViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = District.objects.all().order_by('id')
    serializer_class = DistrictSerializer
    permission_classes = [permissions.IsAuthenticated]


class DistrictGroupByViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = District.objects.distinct('state')
    serializer_class = DistrictGroupBySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ids = self.request.query_params.get('ids', None)
        if ids is not None:
            ids = [ int(x) for x in ids.split(',') ]
            queryset = District.objects.filter(state__in=ids).distinct('state')

        else:
            queryset = District.objects.distinct('state')[0:10]

        return queryset
    
class CityGroupByViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = City.objects.distinct('district')
    serializer_class = CityGroupBySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        ids = self.request.query_params.get('ids', None)
        if ids is not None:
            ids = [ int(x) for x in ids.split(',') ]
            queryset = City.objects.filter(district__in=ids).distinct('district')

        else:
            queryset = City.objects.distinct('district')[0:10]

        return queryset

