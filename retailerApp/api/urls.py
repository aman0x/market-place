from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet, basename='retailer')
router.register(r'retailer_number', views.RetailerNumberViewSet, basename='retailer')
router.register(r'add_to_cart', views.AddToCart, basename='add_to_cart')
router.register(r'checkout', views.Checkout, basename='checkout')
# router.register(r'notification', views.RetailerNotification, basename='retailer_notification')

urlpatterns = [
    path('', include(router.urls)),
    path('data/wholeseller/<int:wholeseller_id>/', views.WholesellerIdRetailerAPIView.as_view(),name="all-retailer-details-under-Wholeseller"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/', views.WholesellerIdRetailerIdViewSet.as_view(),name="retailer-details-under-Wholeseller"),
    path('details/<int:retailer_number>/', views.RetailerDetailsByNumberViewSet.as_view({'get': 'list'}), name="retailer-details-under-one-number"),
    path('verify_phone/', views.RetailerVerifyNumber.as_view(), name="retailer-login"),
    path('verify_otp/', views.RetailerVerifyOTP.as_view(), name='verify_otp'),
    # path(),
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
