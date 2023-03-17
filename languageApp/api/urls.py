from django.urls import path, include
from rest_framework import routers
from .views import LanguageViewSet


router = routers.DefaultRouter()
router.register('list', LanguageViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
