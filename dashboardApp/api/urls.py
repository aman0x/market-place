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
    path('', include(router.urls)),
]

urlpatterns += router.urls
