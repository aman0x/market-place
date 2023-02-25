from django.urls import path,include
from rest_framework import routers
from.import views

router=routers.DefaultRouter()
router.register(r'data',views.Planviewset),


urlpatterns=[
    path('',include(router.urls)),
]