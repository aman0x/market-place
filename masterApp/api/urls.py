from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'unit', views.UnitViewSet)
router.register(r'wholeseller-type', views.WholesellerTypeViewSet)
router.register(r'retailer-type', views.RetailerTypeViewSet)
router.register(r'colour', views.ColourViewSet)
router.register(r'size', views.SizeViewSet)


urlpatterns = [
    path('', include(router.urls)),
]