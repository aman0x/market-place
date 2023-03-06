from rest_framework import serializers
from account.models import UserPayment, Account
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, force_bytes, DjangoUnicodeDecodeError
from django.contrib.sites.shortcuts import get_current_site
from account.api.task import util
from django.contrib.auth import get_user_model
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_static.models import StaticDevice
from phonenumbers import parse
from django_otp import user_has_device
from phonenumbers import parse, NumberParseException






User = get_user_model()


class UserPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPayment
        fields = "__all__"


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["user", "description", "user_type", "locality"]


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


    def validate_phone(self, value):
        try:
            phone_number = parse(value, None)
        except NumberParseException:
            raise serializers.ValidationError('Invalid phone number format')

        account = self.context['request'].user.account

        if user_has_device(account.user, TOTPDevice):
            raise serializers.ValidationError('OTP device already registered')

        device = TOTPDevice.objects.create(
            user=account.user,
            name='Mobile device',
            confirmed=True,
            key=None,
            digits=6,
            tolerance=1,
        )

        device.config_url = 'otpauth://totp/{0}:{1}?secret={2}&issuer={0}'.format(
            'Your App Name',
            phone_number.national_number,
            device.bin_key
        )
        device.save()

        account.phone = phone_number
        account.device_id = device.persistent_id
        account.save()

        return value


    
class UserPasswordResetSerialzer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    # Validating Password and Confirm Password while Change Password
    def validate(self, attrs):
        try:
            uid = self.context.get('uid')
            token = self.context.get('token')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't matched")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')


class SendPasswordSerializers(serializers.Serializer):
    email = serializers.EmailField(max_length=30)

    class Meta:
        fields = ["email"]

    def validate(self, attrs):
        email = attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('Encoded UID', uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('Password Reset Token', token)
            link = 'http://localhost:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link', link)
            # Send Email
            body = 'Click Following Link to Reset Your Password '+link
            data = {
                'subject': 'Reset Your Password',
                'body': body,
                'to_email': user.email
            }
            util.send_email(data)
        return attrs

    def create(self, validated_data):
        return User.objects.all(**validated_data)


class UserPasswordResetSerialzer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={'input_type': 'password'}, write_only=True)
    confirm_password = serializers.CharField(
        max_length=255, style={'input_type': 'confirm_password'}, write_only=True)

    class Meta:
        fields = ['password', 'confirm_password']

    def validate(self, attrs):
        try:
            uid = self.context.get('uid')
            token = self.context.get('token')
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError(
                    "Password and Confirm Password doesn't matched")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError(
                    'Token is not Valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user, token)
            raise serializers.ValidationError('Token is not Valid or Expired')
