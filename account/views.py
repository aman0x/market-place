from rest_framework import viewsets,status
from rest_framework.decorators import action
from rest_framework.response import Response
from.models import *
from.serializers import AccountSerializer
from django.utils.crypto import get_random_string
from django.contrib.auth import authenticate
#from account.send_otp import send_otp_phone


class LoginViewOtp(viewsets.ModelViewSet):
    queryset=Account.objects.all()
    serializer_class=AccountSerializer

    #def create(self, request):
     #   serializer = self.serializer_class(data=request.data)
      #  serializer.is_valid(raise_exception=True)

       # phone = serializer.validated_data['phone']
        #otp = serializer.validated_data['otp']
        #user_type = serializer.validated_data['user_type']
        #user = authenticate(request=request, phone=phone, otp=otp, user_type=user_type)

        #if user is not None:
         #   user=Account.objects.create(phone=phone)
          #  return Response({'success': True})
        #else:
         #   return Response({'success': False}, status=status.HTTP_401_UNAUTHORIZED)  


    @action(detail=False, methods=['post'])
    def login_with_otp(self, request):
        user_type = request.data.get('user_type')
        otp = request.data.get('otp')
        user = authenticate(request, user_type=user_type, otp=otp)
        if user:
            return Response({'detail': 'Login successful'})
        else:
            return Response({'detail': 'Invalid credentials'})