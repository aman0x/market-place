from django.urls import path,include
from rest_framework import routers
from .import views
#from .views import SendPasswordResetView
router=routers.DefaultRouter()
router.register(r'payment',views.UserPaymentViewset)
router.register(r'account',views.AccountViewset)
router.register(r'send-email',views.PasswordResetEmailViewSet)
router.register(r'reset-password',views.UserPasswordResetViewset)



urlpatterns=[
     path('',include(router.urls)),
     #path('send-reset-password-email/', SendPasswordResetView.as_view(), name='send-reset-password-email'),
     path('otp-login/',views.OTPLoginView.as_view()),



]