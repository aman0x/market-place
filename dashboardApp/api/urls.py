from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()

router.register(r'summary', views.SummaryViewSet, 'bazaar-summary')
router.register(r'report', views.BazaarReportViewSet, 'bazaar-report')
router.register(r'plan', views.PlansViewSet, 'bazaar-plans')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
