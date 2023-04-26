from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
