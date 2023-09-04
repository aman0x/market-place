from rest_framework import viewsets
from rest_framework import permissions
from languageApp.models import Language
from .serializers import languageSerializer

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = languageSerializer
    permissions_classes = [permissions.IsAuthenticated]
    