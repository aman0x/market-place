from rest_framework import viewsets, views

from rest_framework import permissions
from .serializers import BazaarReportSerializer, PlansSerializer, SummarySerializer
from bazaarApp.models import Bazaar
from rest_framework.response import Response


class SummaryViewSet(views.APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        data = {"bazaar": 10, "wholeseller": 130, "revenue": 10, "bill": 12310, "agent": 10, "commission": 1230, "customer": 11320}
        results = SummarySerializer(data).data
        return Response(results)


class BazaarReportViewSet(views.APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {"wholeseller": 10, "revenue": 130, "bill": 10,
                "agent": 12310, "commission": 1230, "customer": 11320}
        results = BazaarReportSerializer(data).data
        return Response(results)
    

class PlansViewSet(views.APIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = {"plans": 10, "subscribers": 130, "revenue": 10}
        results = PlansSerializer(data).data
        return Response(results)
