from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet, basename='retailer')
router.register(r'notification', views.RetailerNotification, basename='retailer_notification')
router.register(r'retailer_number', views.RetailerNumberViewSet, basename='retailer')
router.register(r'carts', views.CartViewSet,basename="cartviewset")
router.register(r'subcarts', views.SubCartViewSet,basename="subcartviewset")
router.register(r'click_photo_order', views.ClickPhotoOrderView, basename='click_photo_order')
router.register(r'favorites', views.FavoritesViewSet, basename='favorites')
router.register(r'delivery_addresses', views.DeliveryAddressViewSet, basename='delivery-addresses')
urlpatterns = [
    path('', include(router.urls)),
    #home
    path('details/<int:retailer_number>/',views.RetailerDetailsByNumberViewSet.as_view({'get': 'list', 'post': 'create'}),name="retailer-details-under-one-number"),
    path('details/<int:retailer_number>/<int:pk>/', views.RetailerDetailsByNumberViewSet.as_view({'get': 'list','put': 'update'}),name="retailer-details-update"),

    path('data/wholeseller/<int:wholeseller_id>/', views.WholesellerIdRetailerAPIView.as_view(),name="all-retailer-details-under-Wholeseller"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/', views.WholesellerIdRetailerIdViewSet.as_view(),name="retailer-details-under-Wholeseller"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/offer/', views.RetailerOffer.as_view({'get': 'list'}),name="retailer-offer"),

    #login
    path('verify_phone/', views.RetailerVerifyNumber.as_view(), name="retailer-login"),
    path('verify_otp/', views.RetailerVerifyOTP.as_view(), name='verify_otp'),

    path('subcarts/retailer/<int:retailer_id>/', views.subcart_retailer.as_view({'get': 'list'}), name='sub-cart-retailer'),
    path('carts/retailer/<int:retailer_id>/', views.cart_retailer.as_view({'get': 'list','post': 'create'}), name='cart-retailer'),
    path('update-subcart-used-in-cart/', views.UpdateSubCartUsedInCartView.as_view(), name='update-subcart-used-in-cart'),
    # path('checkout/', views.Checkout.as_view({'get': 'list'}), name='all_product'),

    #create Order
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/category/', views.RetailerIdWholesellerIdCreateOrderNew.as_view({'get': 'list'}),name="wholeseller_category"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/category/<int:category_id>/', views.FilterProductByCategory.as_view(), name="filter-product-by-category"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/allProduct/', views.AllProductByWholesellerId.as_view({'get': 'list'}), name="all-product-by-wholeseller"),
    # path('data/<int:pk>/all_product/', views.AllProductRetailer.as_view({'get': 'list'}), name='all_product'),
]


urlpatterns += router.urls
