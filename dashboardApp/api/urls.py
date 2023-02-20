from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'list', views.GroupViewSet)
router.register(r'bazaar', views.BazarViewSet)
router.register(r'summary', views.SummaryViewSet)
router.register(r'report', views.BazaarReportViewSet)
router.register(r'plans', views.PlansViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]


