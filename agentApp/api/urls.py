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
    path('data/<int:pk>/wholeseller_count/', views.WholesellerCountView.as_view(), name="agent's-wholeseller-count"),
    path('data/<int:pk>/plan_expire/',views.ReportPlanExpireView.as_view(), name="agent's-wholeseller-plan-expiry"),
    path('data/<int:pk>/earning/', views.AgentEarningAPIView.as_view(), name="agent-earning"),
    path('application-status/',views.AgentApplicationStatusViews.as_view(), name="agent-status-message"),
    path('verify_phone/', views.AgentVerifyNumber.as_view(), name="agent-login"),
    path('verify_otp/', views.AgentVerifyOTP.as_view(), name='verify_otp'),
    path('data/<int:pk>/wholeseller-filter/',views.WholesellerFilterViewset.as_view({'get': 'list'}), name="wholeseller-filter"),
    path('', include(router.urls)),
]


