from django.urls import path,include
from rest_framework import routers
from . import views

router=routers.DefaultRouter()
router.register(r'',views.AdsViewset),
router.register(r'referral',views.ReferralViewsets)


urlpatterns=[
    path('',include(router.urls)),
]