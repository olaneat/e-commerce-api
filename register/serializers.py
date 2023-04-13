
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import update_last_login
from rest_framework.response import Response
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from .models import CustomUser
from userProfile.serializers import UserProfileSerializer
#from job.serializers import JobSerializer
#from wallet.serializers import WalletSerializer 

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                ' email & password not found.'
            )

        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
        except user.DoesNotExist:
            raise serializers.ValidationError(
                'user found'
            )

        return {
            'email': user.email,
            'id': user.id,
            'token': jwt_token,
        }
        '''if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
            if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
        }
        '''


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
    )

   # token = serializers.CharField(max_length=255, read_only=True)
    profile = UserProfileSerializer(required=False)
    class Meta:
        model = CustomUser
        fields = ('email',   'username', 'profile', 'password')

    def create(self, validated_data):
        return CustomUser.objects._create_user(**validated_data)

    '''
    def create(request, *args, **kwargs):
        user = CustomUser.objects.create(
            email=request['email'],
            password=request['password']
        )
        user.set_password(request['password'])
        user.save()
        return user
    
    
           '''


class RequestNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=250)

    class Meta:
        fields = ['email']

    def validate(self, attrs):
        try:
            email = attrs.get('email', '')
            if CustomUser.objects.filter(email=email).exists(): 
                user=CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator.make_token(user)
            return attrs
            
        except expression as identifier:
            pass
        return super().validate(attrs)

class CreatePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        min_length=1, max_length=50, write_only=True)
    confirm_password = serializers.CharField(
        min_length=1, max_length=50, write_only=True)
    token = serializers.CharField(
        min_length=1, max_length=50, write_only=True)
    uidb64 = serializers.CharField(
        min_length=1, max_length=250, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')

            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if password != confirm_password:
                raise serializers.ValidationError('password didnt match')

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise Exception()

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(e)

        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        min_length=6, max_length=255, write_only=True)
    new_password = serializers.CharField(
        min_length=6, max_length=255, write_only=True)
    confirm_password = serializers.CharField(
        min_length=6, max_length=255, write_only=True)

    class Meta:
        model = CustomUser
        fields = ('old_password', 'new_password', 'confirm_password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError('password: Password must match')
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old Password not Correct')
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                'You Don\'t have permission to change this password')
        instance.set_password(validated_data['new_password'])
        instance.save()

        res = {
            'instance': instance,
            'message': 'Password successfully Updated',
            'status': status.HTTP_200_OK
        }
        return Response(res)
