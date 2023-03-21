from django.urls import path,include
from rest_framework import routers
from.import views

router=routers.DefaultRouter()
router.register(r'data',views.PlanViewSet),
router.register(r'features',views.FeaturesViewSet),



urlpatterns=[
    path('',include(router.urls)),
    # path('plans/<str:type>/', views.PlanViewSet.as_view({'get': 'list'})),

]