from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.BazarViewSet)
#router.register(r'data',views.Bazaarproductdetailview)
# router.register(r'agent', views.BazarAgentViewSet, 'agent-list')
# router.register(r'wholeseller', views.BazarWholesellerViewSet, 'wholeseller-list')
# router.register(r'product', views.BazarProductViewSet, 'product-list')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]


