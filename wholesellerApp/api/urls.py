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
    path('application-status/', views.WholesellerApplicationStatusViews.as_view(), name="agent-status-message"),
    path('dashboard/', views.WholesellerDashboardViewSet.as_view({'get': 'list'}),name="Wholeseller-dashboard"),
<<<<<<< Updated upstream
    path('dashboard/bazaar/', views.WholesellerDashboardBazzarViewSet.as_view({'get': 'list'}),name="Wholeseller-dashboard-bazzar"),
=======
    path('dashboard/bazaar/', views.WholesellerDashboardBazzarViewSet.as_view({'get': 'list'}),name="Wholeseller-dashboard"),
    path('login', views.WholesalerLogin.as_view(), name="wholesaler-login")
>>>>>>> Stashed changes
]

urlpatterns += router.urls
