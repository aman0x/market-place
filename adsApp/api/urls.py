from django.urls import path,include
from rest_framework import routers
from.import views

router=routers.DefaultRouter()
router.register(r'',views.AdsViewSets)


urlpatterns=[
    path('',include(router.urls)),
    path('',views.StateViewSet.as_view({"get"})),
]