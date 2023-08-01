from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'data', views.RetailerViewSet, basename='retailer')
router.register(r'notification', views.RetailerNotification, basename='retailer_notification')
router.register(r'retailer_number', views.RetailerNumberViewSet, basename='retailer_number')
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

    #create Order
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/category/', views.RetailerIdWholesellerIdCreateOrderNew.as_view({'get': 'list'}),name="wholeseller_category"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/category/<int:category_id>/', views.FilterProductByCategory.as_view(), name="filter-product-by-category"),
    path('data/<int:retailer_id>/wholeseller/<int:wholeseller_id>/create_new_order/allProduct/', views.AllProductByWholesellerId.as_view({'get': 'list'}), name="all-product-by-wholeseller"),

    #orders
    path('recent_order/retailer/<int:retailer_id>/', views.recent_order.as_view({'get': 'list'}), name="recent_order"),
    path('completed_order/retailer/<int:retailer_id>/', views.completed_order.as_view({'get': 'list'}), name="completed_order"),
    path('pending_order/retailer/<int:retailer_id>/', views.pending_order.as_view({'get': 'list'}), name="pending_order"),

    # nav-bar
    path('nav_notification/retailer/<int:retailer_id>/', views.nav_notification.as_view({'get': 'list'}), name='nav_notification'),
    # reports
    path('report/retailer/<int:retailer_id>/orders/', views.report_orders.as_view({'get': 'list'}), name='report_order'),
    path('report/retailer/<int:retailer_id>/orders_details/', views.report_orders_cart.as_view({'get': 'list'}), name='report_order_details'),
    path('report/retailer/<int:retailer_id>/products/', views.report_product.as_view({'get': 'list'}), name='report_product'),
    path('report/retailer/<int:retailer_id>/products_top_product/', views.report_products_top_product.as_view({'get': 'list'}), name='report_product'),
    path('report/retailer/<int:retailer_id>/payments/', views.report_payment.as_view({'get': 'list'}), name='report_payment'),

    # my performance
    path('<int:retailer_id>/my_performance/', views.my_performance.as_view({'get': 'list'}), name='my_performance'),
    #Payments
    # my transactions
    path('<int:retailer_id>/my_transactions/', views.my_transactions.as_view({'get': 'list'}), name='my_transactions'),
    # credit details
    path('<int:retailer_id>/credit_details/', views.credit_details.as_view({'get': 'list'}), name='credit_details'),






]


urlpatterns += router.urls
