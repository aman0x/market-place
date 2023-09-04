from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.ProductAPIView)
router.register(r'filter', views.ProductFilterAPIView)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('unit/', views.ProductUnitAPIView.as_view(), name="unit"),
    path('weight/', views.ProductWeightAPIView.as_view(), name="weight"),
    path('', include(router.urls)),
]
