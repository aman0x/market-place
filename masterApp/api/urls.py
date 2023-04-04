from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'unit', views.UnitViewSet)
router.register(r'wholeseller-type', views.WholesellerTypeViewSet)
router.register(r'retailer-type', views.RetailerTypeViewSet)


urlpatterns = [
    path('', include(router.urls)),
   
]