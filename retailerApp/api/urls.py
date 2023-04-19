from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.WholesellerViewSet),
# router.register(r'dash', views.WholesellerDashboardViewSet),


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', views.WholesellerDashboardViewSet.as_view({'get': 'list'}),name="Wholeseller-dashboard"),
    path('dashboard/bazaar/', views.WholesellerDashboardBazzarViewSet.as_view({'get': 'list'}),name="Wholeseller-dashboard"),
]

urlpatterns += router.urls
