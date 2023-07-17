from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet, basename='retailer')
router.register(r'add_to_cart', views.AddToCart, basename='add_to_cart')
router.register(r'checkout', views.Checkout, basename='checkout')

urlpatterns = [
    path('', include(router.urls)),
    path('data/', views.RetailerViewSet.as_view({'get': 'list'}), name="retailer_data"),
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
    # path('data/<int:pk>/all_product/', views.AllProductRetailer.as_view({'get': 'list'}), name='all_product'),
    # path('checkout/', views.Checkout.as_view({'get': 'list'}), name='all_product'),

    # Orders

    # Payments


]

urlpatterns += router.urls
