from drf_yasg import openapi
from drf_yasg.openapi import (IN_QUERY, TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING,
                              Parameter, Schema)

from .serializers import UserSerializer

# Payload Definitions
FIRST_NAME = openapi.Schema(
    type=openapi.TYPE_STRING, description='First name of the user')
LAST_NAME = openapi.Schema(type=openapi.TYPE_STRING,
                           description='Last name of the user')
AGE = openapi.Schema(type=openapi.TYPE_INTEGER, description="User's age")
EMAIL = openapi.Schema(type=openapi.TYPE_STRING,
                       description="Email address of the user")
PASSWORD = openapi.Schema(type=openapi.TYPE_STRING, description="Password")

# Error Message DEFINITIONS
HTTP_409 = {'error': 'User already registered'}
HTTP_403 = {
    'error': 'can not authenticate with the given credentials or the account\
 has been deactivated'}
HTTP_400 = {'error': 'please provide a email and a password'}
HTTP_500 = {'error': "Internal server error"}


# Swagger Responses
RESP_403 = openapi.Response(description="Authentication Failed",
                            examples={"application/json": HTTP_403})
RESP_400 = openapi.Response(description="Invalid payload",
                            examples={"application/json": HTTP_400})
RESP_409 = openapi.Response(description="User already available",
                            examples={"application/json": HTTP_409})
RESP_500 = openapi.Response(description="Server Error",
                            examples={"application/json": HTTP_500})


# Swagger Payload
REQ_USER_PAYLOAD = Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'first_name': FIRST_NAME,
        'last_name': LAST_NAME,
        'age': AGE,
        'email': EMAIL,
        'password': PASSWORD,
    })

AUTH_PAYLOAD = Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': EMAIL,
        'password': PASSWORD,
    })

CREATE_USER = {
    'response': {
        201: UserSerializer,
        409: RESP_409
    },
    'request_body': REQ_USER_PAYLOAD
}

PUT_USER = {
    'response': {
        200: UserSerializer
    },
    'request_body': REQ_USER_PAYLOAD
}

AUTH_USER = {
    'response': {
        400: RESP_400,
        403: RESP_403,
        500: RESP_500
    },
    'request_body': AUTH_PAYLOAD
}
