from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from .views import index
from django.conf.urls.static import static
from rest_framework_simplejwt import views as jwt_views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import routers
from bazaarApp.api.views import BazarViewSet
from agentApp.api.views import AgentViewSet
from wholesellerApp.api.views import WholesellerViewSet
from parentCategoryApp.api.views import ParentCategoryAPIView
from categoryApp.api.views import CategoryAPIView
from subCategoryApp.api.views import SubCategoryAPIView
from productApp.api.views import ProductAPIView
from profileApp.api.views import UserViewSet





admin.site.site_header = settings.ADMIN_SITE_HEADER
router = routers.DefaultRouter()

urlpatterns = [
    path(r'api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path(r'api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path(r'api/login/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(r'api/bazaar/', include('bazaarApp.api.urls')),
    path(r'api/agent/', include('agentApp.api.urls')),
    path(r'api/wholeseller/', include('wholesellerApp.api.urls')),
    path(r'api/parentcategory/', include('parentCategoryApp.api.urls')),
    path(r'api/category/', include('categoryApp.api.urls')),
    path(r'api/subcategory/', include('subCategoryApp.api.urls')),
    path(r'api/product/', include('productApp.api.urls')),
    path(r'api/agency/',include('agencyApp.api.urls')),
    path(r'api/plans/',include('planApp.api.urls')),
    path(r'api/ads/',include('adsApp.api.urls')),
    path(r'api/user/',include('profileApp.api.urls')),
    path(r'api/account/',include('account.api.urls')),
    path(r'api/orders/',include("orderApp.api.urls")),
    path(r'api/location/',include("locationApp.api.urls")),
    
    # path(r'api/account/', include('account.api.urls')),
    # path(r'api/bucket/', include('bucket.api.urls'),  name='site_info'),
    # path(r'api/itemmaster/', include('itemmaster.api.urls')),
    # path(r'api/category/', include('category.api.urls')),
    # path(r'api/subcategory/', include('subcategory.api.urls')),
    # path(r'api/locality/', include('locality.api.urls')),
    # path(r'api/order/', include('order.api.urls')),
    # path(r'api/invoice/', include('invoice.api.urls')),
    path(r'api/dashboard/', include('dashboardApp.api.urls')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
