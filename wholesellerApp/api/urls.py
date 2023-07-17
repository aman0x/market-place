from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.WholesellerViewSet),

# -------------wholeseller branch-------
router.register(r'branch', views.WholesellerBranchViewSet),
router.register(r'data/branch/add_product', views.WholesellerBranchAddProduct),
# router.register(r'data/branch/category_wise_plan_list', views.WholesellerBranchCategoryWisePlanList),

# ------------wholeseller agent-----------
router.register(r'agent', views.WholesellerAgentViewSet)

# -------------Wholeseller Orders---------
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'editorders', views.EditOrderViewSet, basename='edit_order')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('verify_phone/', views.WholesellerVerifyNumber.as_view(), name="wholseller-login"),
    path('verify_otp/', views.WholesellerVerifyOTP.as_view(), name='verify_otp'),
    path('application-status/', views.WholesellerApplicationStatusViews.as_view(), name="agent-status-message"),
    path('dashboard/', views.WholesellerDashboardViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard"),
    path('dashboard/bazaar/', views.WholesellerDashboardBazzarViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard-Bazaar"),
    path('dashboard/', views.WholesellerDashboardViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard"),
    path('data/<int:pk>/bazaar-list/', views.WholesellerBazaarListViewSet.as_view({'get': 'list'}), name="Wholeseller-bazaar-list"),
    path('data/<int:pk>/bazaar-list/<int:bazaar_id>/product/', views.WholesellerBazaarProductViewSet.as_view({'get': 'list'}), name="Wholeseller-bazaar-product-list"),
    path('data/<int:pk>/bazaar-list/<int:bazaar_id>/', views.WholesellerBazaarViewSet.as_view({'get': 'list'}), name="Wholeseller-bazaar-details"),
    path('data/<int:pk>/dashboard/total-product/', views.WholesellerDashboardTotalProductViewSet.as_view(), name="Wholeseller-dashboard-Total-Product"),
    path('data/<int:pk>/dashboard/total-order/', views.WholesellerDashboardTotalOrderViewSet.as_view(), name="Wholeseller-dashboard-total_order"),
    path('data/<int:pk>/dashboard/total-income/', views.WholesellerDashboardTotalIncomeViewSet.as_view(), name="Wholeseller-dashboard-total_income"),
    path('data/<int:pk>/dashboard/new-retailers/', views.WholesellerDashboardNewRetailersViewSet.as_view(), name="Wholeseller-dashboard-new-retailers"),
    path('data/<int:pk>/dashboard/top-retailers/',views.WholesellerDashboardTopRetailersViewSet.as_view({'get': 'list'}), name="Wholeseller-dashboard-top-retailers"),
    path('data/<int:pk>/dashboard/top-products/', views.WholesellerDashboardTopProductsViewSet.as_view(), name="Wholeseller-dashboard-top-products"),
    path('data/<int:pk>/dashboard/categories/', views.WholesellerDashboardCategoriesViewSet.as_view(), name="Wholeseller-dashboard-categories"),
    path('data/<int:pk>/dashboard/sub-categories/', views.WholesellerDashboardSubCategoriesViewSet.as_view(), name="Wholeseller-dashboard-sub-categories"),
    path('data/<int:pk>/dashboard/ads-performance/', views.WholesellerDashboardAdsPerformanceViewSet.as_view(), name="Wholeseller-dashboard-ads-performance"),
    path('data/<int:pk>/dashboard/top-branches/', views.WholesellerDashboardTopBranchesViewSet.as_view(), name="Wholeseller-dashboard-top-branches"),
    path('data/<int:pk>/product/', views.WholesellerProductViewSet.as_view(), name="Wholeseller-Product"),
    path('data/<int:pk>/report/total-order/', views.WholesellerReportTotalOrderViewSet.as_view(), name="Wholeseller-Report-total_order"),
    path('data/<int:pk>/report/total-income/', views.WholesellerReportTotalIncomeViewSet.as_view(), name="Wholeseller-Report-total_income"),
    path('data/<int:pk>/report/city-wise-business/', views.WholesellerReportCityWiseBusinessViewSet.as_view({'get': 'list'}), name="Wholeseller-Report-city-wise-business"),
    path('data/<int:pk>/report/top-products/', views.WholesellerReportTopProductViewSet.as_view(), name="Wholeseller-Report-top-product"),
    path('data/<int:pk>/report/new-retailers/', views.WholesellerReportRetailersViewSet.as_view(), name="Wholeseller-Report-new-retailers"),
    path('data/<int:pk>/report/transaction-history/', views.WholesellerReportTransactionViewSet.as_view(), name="Wholeseller-Report-transaction-history"),
    path('data/<int:pk>/report/realtime-sale/', views.WholesellerReportRealtimeSaleViewSet.as_view(), name="Wholeseller-Report-realtime-sale"),
    # path('data/<int:pk>/bazaar-list/', views.WholesellerBazaarListViewSet.as_view(), name="Wholeseller-Bazaar-List"),

    # ----------------- Wholeseller branch-----------

    path('data/branch/verify_phone/', views.WholesellerBranchManagerVerifyNumber.as_view(), name="wholeseller-retailer-login"),
    path('data/branch/verify_otp/', views.WholesellerBranchManagerVerifyOTP.as_view(), name='wholeseller-retailer-verify_otp'),


    path('data/branch/<int:branch_id>/categorylist/', views.WholesellerBranchCategoryList.as_view(), name='wholeseller-branch-category-list'),
    path('data/branch/category-wise-plan/', views.WholesellerBranchCategoryWisePlanList.as_view({'get': 'list', 'post': 'create'}), name='wholeseller-branch-category-wise-plan'),
    path('data/branch/category-wise-plan/<int:pk>/', views.WholesellerBranchCategoryWisePlanList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wholeseller-branch-category-wise-plan-detail'),

    path('data/branch/<int:branch_id>/subcategorylist/', views.WholesellerBranchSubCategoryList.as_view(), name='wholeseller-branch-subcategory-list'),
    path('data/branch/sub-category-wise-plan/', views.WholesellerBranchSubCategoryWisePlanList.as_view({'get': 'list', 'post': 'create'}), name='wholeseller-branch-sub-category-wise-plan'),
    path('data/branch/sub-category-wise-plan/<int:pk>/', views.WholesellerBranchSubCategoryWisePlanList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wholeseller-branch-sub-category-wise-plan-detail'),

    path('data/branch/<int:branch_id>/itemlist/', views.WholesellerBranchItemList.as_view(), name='wholeseller-branch-item-list'),
    path('data/branch/item-wise-plan/', views.WholesellerBranchItemWisePlanList.as_view({'get': 'list', 'post': 'create'}), name='wholeseller-branch-item-wise-plan'),
    path('data/branch/item-wise-plan/<int:pk>/', views.WholesellerBranchItemWisePlanList.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wholeseller-branch-item-wise-plan-detail'),

    path('data/branch/<int:branch_id>/productPricing/', views.WholesellerBranchProductPricingViews.as_view({'get': 'list', 'post': 'create'}), name='wholeseller-branch-item-list'),
    path('data/branch/<int:branch_id>/productPricing/<int:pk>/', views.WholesellerBranchProductPricingViews.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='wholeseller-branch-item-list'),

    # ----------------- Wholeseller agent-----------
    # path('agent/<int:pk>/wholeseller_count/', views.WholesellerCountView.as_view(), name="agent's-wholeseller-count"),
    path('data/<int:pk>/agent/application_status/', views.WholesellerAgentApplicationStatusViews.as_view(), name="wholeseller-agent-status-message"),
    path('data/agent/verify_phone/', views.WholesellerAgentVerifyNumber.as_view(), name="wholeseller-agent-login"),
    path('data/agent/verify_otp/', views.WholesellerAgentVerifyOTP.as_view(), name='wholeseller-verify_otp'),

    path('data/<int:wholeseller_id>/agent/', views.WholesellerIdAgentViewSet.as_view({'get': 'list'}), name="all-agent-details-under-Wholeseller"),
    path('data/<int:wholeseller_id>/agent/<int:agent_id>/', views.WholesellerIdAgentViewSetIdViewSet.as_view(), name="agent-details-under-Wholeseller"),

]

urlpatterns += router.urls
