from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.WholesellerViewSet),
# router.register(r'dash', views.WholesellerDashboardViewSet),


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('application-status/', views.WholesellerApplicationStatusViews.as_view(), name="agent-status-message"),
    path('dashboard/', views.WholesellerDashboardViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard"),
    path('dashboard/bazaar/', views.WholesellerDashboardBazzarViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard-Bazaar"),
    path('data/<int:pk>/product/', views.WholesellerProductViewSet.as_view(), name="Wholeseller-Product"),
    path('data/<int:pk>/report/total-order/', views.WholesellerReportTotalOrderViewSet.as_view(), name="Wholeseller-Report-total_order"),
    path('data/<int:pk>/report/total-income/', views.WholesellerReportTotalIncomeViewSet.as_view(), name="Wholeseller-Report-total_income"),
    path('data/<int:pk>/report/city-wise-business/', views.WholesellerReportCityWiseBusinessViewSet.as_view({'get': 'list'}), name="Wholeseller-Report-city-wise-business"),
    path('data/<int:pk>/report/top-products/', views.WholesellerReportTopProductViewSet.as_view(), name="Wholeseller-Report-top-product"),
    path('data/<int:pk>/report/new-retailers/', views.WholesellerReportRetailersViewSet.as_view(), name="Wholeseller-Report-new-retailers"),
    path('data/<int:pk>/report/transaction-history/', views.WholesellerReportTransactionViewSet.as_view(), name="Wholeseller-Report-transaction-history"),
    path('data/<int:pk>/report/realtime-sale/', views.WholesellerReportRealtimeSaleViewSet.as_view(), name="Wholeseller-Report-realtime-sale"),
]

urlpatterns += router.urls
