from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.BazarViewSet),
router.register(r'csv',views.ProductCsvViewSet),

# router.register(r'agent', views.BazarAgentViewSet, 'agent-list')
# router.register(r'wholeseller', views.BazarWholesellerViewSet, 'wholeseller-list')
# router.register(r'product', views.BazarProductViewSet, 'product-list')
# router.register(r'top-product',views.BazarProductsListViewSet)
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = [
    path('data/<int:pk>/total-orders/', views.BazarViewReportTotalOrdersViewSet.as_view({'get': 'list'}),name="total-orders"),
    path('data/<int:pk>/total-income/', views.BazarViewReportTotalIncomeViewSet.as_view({'get': 'list'}),name="total-income"),
    path('data/<int:pk>/city-wise/', views.BazarViewReportCityWiseViewSet.as_view({'get': 'list'}),name="city-wise"),
    path('data/<int:pk>/top-wholesellers/', views.BazarViewReportTopWholesellersViewSet.as_view({'get': 'list'}),name="top-wholesellers"),
    path('data/<int:pk>/top-products/', views.BazarViewReportTopProductsViewSet.as_view({'get': 'list'}),name="top-products"),
    path('data/<int:pk>/new-wholesellers/', views.BazarViewReportNewWholesellersViewSet.as_view({'get': 'list'}),name="new-wholesellers"),
    path('data/<int:pk>/wholesellers-list/', views.BazarWholesellersListViewSet.as_view({'get': 'list'}),name="wholesellers-List"),
    path('data/<int:pk>/agents-list/', views.BazarAgentsListViewSet.as_view({'get': 'list'}),name="agents-List"),
    path('data/<int:pk>/products-list/', views.BazarProductsListViewSet.as_view({'get': 'list'}),name="products-List"),
    path('data/<int:pk>/dashboard/', views.BazarDashboardViewSet.as_view({'get': 'list'}),name="products-List"),
    path('data/<int:pk>/retailer-type/', views.BazarRetailerTypeViewSet.as_view({'get': 'list'}),name="retailer-"),
    path('', include(router.urls))
]

urlpatterns += router.urls

