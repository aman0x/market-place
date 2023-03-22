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

admin.site.site_header = settings.ADMIN_SITE_HEADER
router = routers.DefaultRouter()

urlpatterns = [
    path(r'api/login/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
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
    path(r'api/orders/',include("orderApp.api.urls")),
    path(r'api/location/',include("locationApp.api.urls")),
    path(r'api/lan/', include('languageApp.api.urls')),
    path(r'api/dashboard/', include('dashboardApp.api.urls')),
    path(r'api/payment/',include('paymentApp.api.urls')),
    path('admin/', admin.site.urls),
    path('', include(router.urls))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
