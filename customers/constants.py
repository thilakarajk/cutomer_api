from drf_yasg import openapi
from drf_yasg.openapi import (IN_PATH, TYPE_INTEGER, TYPE_OBJECT, TYPE_STRING,
                              Parameter, Schema)

from .serializers import CustomerSerializer

# Payload Definitions
FIRST_NAME = Schema(title='First Name',
                    type=TYPE_STRING, description='First name of the Customer')
LAST_NAME = Schema(type=TYPE_STRING, title='Last Name',
                   description='Last name of the Customer')
NAME = Schema(type=TYPE_STRING,
              description='Full name of the Customer')
AGE = Schema(type=TYPE_INTEGER, description="Customer's age")
EMAIL = Schema(type=TYPE_STRING,
               description="Email address of the Customer")

# Error Message DEFINITIONS
HTTP_404 = {'error': 'Customer does not exist'}
HTTP_400 = {'error': 'please check your payload'}
HTTP_500 = {'error': "Internal server error"}
HTTP_204_DELETE = {"status": "Deleted Successfully"}
HTTP_204 = CustomerSerializer
HTTP_200 = CustomerSerializer
HTTP_201 = CustomerSerializer

# Swagger Response
RESP_404 = openapi.Response(description="No customers found",
                            examples={"application/json": HTTP_404})
RESP_400 = openapi.Response(description="Invalid payload",
                            examples={"application/json": HTTP_400})


# Swagger Payload and Params
PARAM_ID = Parameter('id', IN_PATH, 'Customer Id',
                     type=TYPE_STRING, required=True)
REQ_CUSTOMER_PAYLOAD = Schema(
    type=TYPE_OBJECT,
    properties={
        'name': NAME,
        'first_name': FIRST_NAME,
        'last_name': LAST_NAME,
        'age': AGE,
        'email': EMAIL
    })
# Swagger Schema

GET_CUSTOMER_SINGLE = {
    "response": {
        200: HTTP_200,
        404: RESP_404
    },
    "params": [PARAM_ID]
}

PUT_CUSTOMER_SINGLE = {
    "response": {
        404: RESP_404,
        204: HTTP_204,
        400: RESP_400
    },
    "request_body": REQ_CUSTOMER_PAYLOAD,
    "params": [PARAM_ID]
}

DELETE_CUSTOMER_SINGLE = {
    "params": [PARAM_ID],
    "response": {
        404: RESP_404
    }
}

POST_CUSTOMER = {
    'response': {
        201: HTTP_201
    },
    'request_body': REQ_CUSTOMER_PAYLOAD
}
