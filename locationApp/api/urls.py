from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'state', views.StateViewSet)
router.register(r'city', views.CityViewSet)
router.register(r'district', views.DistrictViewSet)
router.register(r'g-dist', views.DistrictGroupByViewSet)
router.register(r'g-city', views.CityGroupByViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path(r'^g-dist/', views.DistrictGroupByViewSet.as_view({'get': 'list'}),name="groupbydist"),
]