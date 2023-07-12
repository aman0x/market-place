from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify_phone/', views.RetailerVerifyNumber.as_view(), name="retailer-login"),
    path('verify_otp/', views.RetailerVerifyOTP.as_view(), name='verify_otp'),
]

urlpatterns += router.urls
