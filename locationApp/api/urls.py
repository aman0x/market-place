from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'state', views.StateViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'district', views.DistrictViewSet)

urlpatterns = [
    path('', include(router.urls)),
]