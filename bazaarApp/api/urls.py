from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.BazarViewSet)
router.register(r'agent', views.BazarAgentViewSet)
router.register(r'wholeseller', views.BazarWholesellerViewSet)
router.register(r'product', views.BazarProductViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]


