
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
#from rest_framework.decorators import api_view
from rest_framework import generics, viewsets, status
from rest_framework import permissions 
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.exceptions import ValidationError
from .serializers import (
    RegistrationSerializer, CreatePasswordSerializer, 
    ChangePasswordSerializer, LoginSerializer, 
    RequestNewPasswordSerializer
)
from register.models import CustomUser
from register import serializers
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Utils


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer


class RegistrationAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = request.data
            email = data.get('email')
            password = data.get('password')
            response = {
                'success': True,
                'message': "signup successful, proceed to login",
                'status_code': status.HTTP_201_CREATED,
                'username': serializer.data.get('username', None),
                'email': serializer.data.get('email', None),
            }
            return Response(response)
        except ValidationError as e:
            error_messages = []
            for field, errors in e.detail.items():
                if isinstance(errors, list):
                    error_messages.extend(errors)
                else:
                    error_messages.append(str(errors))
            message = '; '.join(error_messages) if error_messages else 'Validation error'
            return Response({
                'success': False,
                'message': message,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'errors': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'login successful',
                    'refresh_token': str(refresh),
                    'access_token': str(refresh.access_token),
                    #'token':  serializer.data['token'],
                    "user": {
                            'firstName':self.request.user.user_profile.first_name,
                            'lastName': self.request.user.user_profile.last_name,
                            'id': self.request.user.id,
                            'email': self.request.user.email,
                            'username': self.request.user.username,
                        }
                    # 'first_name': self.request.user.user_profile.first_name,
                    # 'last_name': self.request.user.user_profile.last_name,
                    # 'id': self.request.user.id,
                    # 'email': self.request.user.email,
                    # 'is_admin': self.request.user.is_superuser,
                }
                status_code = status.HTTP_200_OK
                #print(data)
                return Response(response, status=status_code)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class changePasswordAPIView(generics.UpdateAPIView):
    models = CustomUser
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = CreatePasswordSerializer

    def get_obj(self, queury_set=None):
        obj = self.request.user

    def update(self, request, *arg, **kwargs):
        self.object = self.get_obj()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not self.object.check_password(serializer.data.get('old_password')):
                return Response(
                    {"old_password": ["Invalid password"]},
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.object.set_password(new_password)
            self.object.save()
            response = {
                'message': 'Password Successfully Changed',
                'code': status.HTTP_200_OK,
                'status': 'Success', 
            }

            return Response(response)

        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetAPIView(generics.GenericAPIView):
    serializer_class = RequestNewPasswordSerializer

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        email = request.data['email']
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            dRelativeLink = reverse(
                'register:password-reset-confirmed', kwargs={'uidb64': uidb64, 'token': token})
            django_absUrl = 'http://' + current_site + dRelativeLink

            local_host = 'http://localhost:4200/account/'
            relativeLink = 'change-password/'+uidb64+' /'+token
            absUrl = local_host+relativeLink
            body = 'Hi  Click on the Link below to change your password \n' + absUrl
            data = {
                'body': body, "recipient": user.email,
                "subject": "Password Reset Link"
            }
            Utils.send_mail(data)
        res = {
            'message': 'Password Reset link sent to Your',
            'status': status.HTTP_200_OK,
            'uidb64': uidb64,
            'token': token
        }
        return Response(res)
        # return super().validate(attrs)


class PasswordTokenAPIView(generics.GenericAPIView):
    def get_queryset(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                res = {'error': 'Invalid Token',
                       'status': status.HTTP_401_UNAUTHORIZED}
                return Response(res)
            res = {'success': True, 'message': 'Done', 'uidb64': uidb64,
                   'token': token, 'status': status.HTTP_200_OK}
            return Response(res)
        except DjangoUnicodeDecodeError as identifer:
            if not PasswordResetTokenGenerator().check_token(user):
                res = {'error': 'Invalid Token',
                       'status': status.HTTP_401_UNAUTHORIZED}
        return Response(res)


class CreatePasswordAPI(generics.GenericAPIView):
    serializer_class = CreatePasswordSerializer

    def patch(self, request):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password changed Successfully'}, status=status.HTTP_200_OK)


# class ChangePasswordAPI(generics.UpdateAPIView):
#     serializer_class = ChangePasswordSerializer
#     queryset = CustomUser.objects.all()
#     permissions_classes = [permissions.IsAuthenticated]


class ChangePasswordAPI(generics.UpdateAPIView):
    models = CustomUser
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def get_obj(self):
        return self.request.user

    def perform_update(self, serializer):
        user = self.get_obj()
        user.set_password(serializer.validated_data['new_password'])
        user.save()

    def update(self, request, *arg, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_update(serializer)
            response = {
                'message': 'Password Successfully Changed',
                'code': status.HTTP_200_OK,
                'status': 'Success', 
            }
        
            return Response(response)

        return Response(
            {
                'message': 'Validation Error',
                'code': status.HTTP_400_BAD_REQUEST,
                'status': 'Error',
                'errors': serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class DisplayUsers(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegistrationSerializer
    permissions_classes = [permissions.AllowAny]


class DeleteUser(generics.DestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = CustomUser.objects.all()  # Define a base queryset

    def get_object(self):
        # Override to get the object based on a lookup (e.g., user ID from URL)
        queryset = self.get_queryset()
        return queryset.get(id=self.kwargs['pk'])  # Assume URL has <pk>

    def get_queryset(self):
        # Optional: Customize queryset if needed
        return self.queryset
