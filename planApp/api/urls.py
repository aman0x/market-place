from django.urls import path,include
from rest_framework import routers
from.import views

router=routers.DefaultRouter()
router.register(r'',views.PlanViewSet)
router.register(r'projects',views.FeaturesProjectViewSet)
router.register(r'subscribers',views.FeaturesSubscribersViewSet)



urlpatterns=[
    path('',include(router.urls)),
    path('plans/<str:type>/', views.PlanViewSet.as_view({'get': 'list'})),

]