import jwt
from django.conf import settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.signals import user_logged_in
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.utils import jwt_payload_handler

from .constants import *
from .models import User
from .serializers import UserSerializer


class CreateUserAPIView(APIView):
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses=CREATE_USER['response'],
        operation_description="API for creating new user to access customer APIs",
        request_body=CREATE_USER['request_body']
    )
    def post(self, request):
        data = request.data
        try:
            User.objects.get(email=data['email'])
            return Response(HTTP_409, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            data['password'] = make_password(data['password'])
            serializer = UserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):

    # Allow only authenticated users to access this url
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @swagger_auto_schema(
        responses=PUT_USER['response'],
        operation_description="API to get current logged user details",
    )
    def get(self, request, *args, **kwargs):
        # serializer to handle turning our `User` object into something that
        # can be JSONified and sent to the client.
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=PUT_USER['response'],
        operation_description='API to modify user details',
        request_body=PUT_USER['request_body']
    )
    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        if hasattr(serializer_data, 'password'):
            serializer_data['password'] = make_password(
                serializer_data['password'])
        serializer = UserSerializer(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(auto_schema=None)
    def patch(self, request):
        # To hide path method in swagger
        pass


class AuthenticateUser(APIView):
    permission_classes = (AllowAny,)

    @swagger_auto_schema(
        responses=AUTH_USER['response'],
        operation_description="Authentication API",
        request_body=AUTH_USER['request_body']
    )
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email']
            password = request.data['password']

            user = User.objects.get(email=email)
            if user and check_password(password, user.password):
                try:
                    payload = jwt_payload_handler(user)
                    token = jwt.encode(payload, settings.SECRET_KEY)
                    user_details = {}
                    user_details['name'] = "%s %s" % (
                        user.first_name, user.last_name)
                    user_details['token'] = token
                    user_logged_in.send(sender=user.__class__,
                                        request=request, user=user)
                    return Response(user_details, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response(HTTP_500, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(HTTP_403, status=status.HTTP_403_FORBIDDEN)
        except KeyError:
            return Response(HTTP_400, status=status.HTTP_400_BAD_REQUEST)
