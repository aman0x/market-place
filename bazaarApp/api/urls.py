from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.BazarViewSet)
#router.register(r'data',views.WhollsellerDetailViewset)
# router.register(r'agent', views.BazarAgentViewSet, 'agent-list')
# router.register(r'wholeseller', views.BazarWholesellerViewSet, 'wholeseller-list')
# router.register(r'product', views.BazarProductViewSet, 'product-list')


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('data/<int:pk>/total-orders/', views.BazarViewReportTotalOrdersViewSet.as_view({'get': 'list'}),name="total-orders"),
    path('data/<int:pk>/total-income/', views.BazarViewReportTotalIncomeViewSet.as_view({'get': 'list'}),name="total-income"),
    path('data/<int:pk>/city-wise/', views.BazarViewReportCityWiseViewSet.as_view({'get': 'list'}),name="city-wise"),
    path('data/<int:pk>/top-wholesellers/', views.BazarViewReportTopWholesellersViewSet.as_view({'get': 'list'}),name="top-wholesellers"),
    path('data/<int:pk>/top-products/', views.BazarViewReportTopProductsViewSet.as_view({'get': 'list'}),name="top-products"),
    path('data/<int:pk>/new-wholesellers/', views.BazarViewReportNewWholesellersViewSet.as_view({'get': 'list'}),name="new-wholesellers"),
]


