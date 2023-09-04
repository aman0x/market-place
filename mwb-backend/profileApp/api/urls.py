from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, 'user')
# router.register(r'groups', views.GroupViewSet, 'user-groups')
# router.register(r'list', views.GroupViewSet, 'user-list')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns += router.urls
