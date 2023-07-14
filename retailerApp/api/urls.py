from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('verify_phone/', views.RetailerVerifyNumber.as_view(), name="retailer-login"),
    path('verify_otp/', views.RetailerVerifyOTP.as_view(), name='verify_otp'),

    # Create order
        #click photo and order
            # image orderId PaymentType
        # crete new order
            # order by category
            # add to cart
            # payment Type
        # all product
    # path('all_product/', views.AllProductRetailer.as_view(), name='all_product'),

    # Orders

    # Payments


]

urlpatterns += router.urls
