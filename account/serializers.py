from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account
import random
from django.conf import settings
from datetime import datetime,timedelta

class AccountSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True, max_length=20)
    otp = serializers.CharField(required=True, max_length=6)
    #class Meta:
       # model=Account
       # fields=["phone",'user_type']
    
    
    
    def validate(self, data):
        phone = data.get('phone_number')
        otp = int(data.get('otp'))
        try:
            account = Account.objects.get(phone=phone)
        except Account.DoesNotExist:
            raise serializers.ValidationError("invalid phone no or otp")
        if account.is_valid_otp(otp) == False:
            raise serializers.ValidationError('invalid phone no or otp')
        if not account.user.is_active:
            raise serializers.ValidationError('user account is disable')
        #data['user'] = User
        data['account'] = account
        return data


    def create(self, validated_data):
        otp = random.randint(100000, 999999)
        otp_expire = datetime.now() + timedelta(minutes=10)
        account = validated_data['account']
        account.otp = otp
        account.otp_expire = otp_expire
        account.save()
        return account    
    
    #def create(self, validated_data):
     #   user = User.objects.create_user(
      #      username=validated_data['user_type'],
       #     password=validated_data['phone']
        #)
        #Account.objects.create(
         #   user=user,
          #  phone=validated_data['phone']
        #)
        #return user
