from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.AgentViewSet)
router.register(r'commision',views.AgentCommisionViewset)
router.register(r'agent-commision-redeem',views.AgentCommisionRedeemViewset)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('report_plan/',views.ReportPlanExpireView.as_view()),
    path('application-status/',views.AgentApplicationStatusViews.as_view()),
    path('verify_phone/', views.AgentVerifyNumber.as_view(), name="agent-login"),
    path('verify_otp/', views.AgentVerifyOTP.as_view(), name='verify_otp'),
    path('', include(router.urls)),
]


