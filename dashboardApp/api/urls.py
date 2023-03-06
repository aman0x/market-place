from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('summary/', views.SummaryViewSet.as_view(), name='bazaar-summary'),
    path('report/', views.BazaarReportViewSet.as_view(), name='report'),
    path('plan/', views.PlansViewSet.as_view(), name='plan'),
    path('plan-list/', views.PlanListViewSet.as_view({'get': 'list'}), name='plan-list'),
    path('bazaar-list/', views.BazaarListViewSet.as_view({'get': 'list'}), name='bazaar-list'),
    path('', include(router.urls)),
]

