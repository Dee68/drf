from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.views import APIView
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from account.serializers import (
    RegisterSerializer,
    EmailvericationSerializer,
    LoginSerializer,
    LogoutSerializer,
    UserSerializer
    )
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from account.models import User, Profile
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
import jwt, datetime


class RegisterView(generics.GenericAPIView):
    """_summary_

    Args:
        APIView (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = RegisterSerializer

    # @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        email_subject = 'Account verification'
        msg = 'please use the link below to verify your account'
        current_site = get_current_site(request).domain
        rel_link = reverse('verify-email')
        abs_link = 'http://'+current_site+rel_link+'?token='+str(token)
        email_body = f'Hi, {user.username}, {msg} {abs_link}'
        data = {
            'user': user.email,
            'subject': email_subject,
            'email_body': email_body,
        }
        Util.send_mail(data)
        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    """_summary_

    Args:
        APIView (_type_): _description_

    Returns:
        _type_: _description_
    """
    serializer_class = EmailvericationSerializer
    token_param_config = openapi.Parameter('token',
                                           in_=openapi.IN_QUERY,
                                           description='Description',
                                           type=openapi.TYPE_STRING
                                           )
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'message':'Acount verified successfully'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error':'Verification token has expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    msg = 'You have succesfully logged in'
    @swagger_auto_schema(operation_description="Enter correct values and log in", responses={200: msg})
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class ProfileApiView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        serializer = UserSerializer(user.profile)
        return Response(serializer.data)
    

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)
    

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    