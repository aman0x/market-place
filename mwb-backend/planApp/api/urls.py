from django.urls import path,include
from rest_framework import routers
from.import views

router=routers.DefaultRouter()
router.register(r'data',views.PlanViewSet),
router.register(r'features',views.FeaturesViewSet),
router.register(r'retailer-plan',views.RetailerPlanViewSet),



urlpatterns=[
    path('',include(router.urls)),
]