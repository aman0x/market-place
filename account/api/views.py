from rest_framework import viewsets,status,generics
from rest_framework import permissions
from account.models import User,Account,UserPayment
from.serializers import UserPaymentSerializer,AccountSerializer,SendPasswordSerializers,LoginSerializer,UserPasswordResetSerialzer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp import login as otp_login
from django.core.exceptions import ObjectDoesNotExist
from account.api.renders import UserRenderer
#from django_otp.plugins.otp_static.models import StaticDevice
# from django.conf import settings
# from django.core.cache import cache
# from django_otp import login as otp_login
# from django_otp import devices_for_user



class AccountViewset(viewsets.ModelViewSet):
    queryset=Account.objects.all().order_by("user_id")
    serializer_class=AccountSerializer
    permission_classes=[permissions.IsAuthenticated]




class OTPLoginView(APIView):
    serializer_class =LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        account = request.user.account

        try:
            device = TOTPDevice.objects.get(user=account.user, persistent_id=account.device_id)
        except ObjectDoesNotExist:
            return Response({'detail': 'OTP device not registered'}, status=status.HTTP_400_BAD_REQUEST)

        otp_login(request, device)

        return Response({'detail': 'OTP login successful'})





class UserPaymentViewset(viewsets.ModelViewSet):
    queryset=UserPayment.objects.all().order_by("id")
    serializer_class=UserPaymentSerializer
    permission_classes=[permissions.IsAuthenticated]
    



class PasswordResetEmailViewSet(viewsets.ModelViewSet):
    serializer_class = SendPasswordSerializers
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def send_password_reset_email(self, request):
        serializer = SendPasswordSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'password reset email sent'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

class UserPasswordResetViewset(viewsets.ModelViewSet):
    serializer_class=UserPasswordResetSerialzer
    queryset=User.objects.all()

    @action(detail=False,methods=['post'])
    def reset_password(self,request):
        serializer=UserPasswordResetSerialzer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status':'reset sucessfully'})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



             







      






