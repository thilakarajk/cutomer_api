from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .constants import *
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.


class GetDeleteUpdateCustomer(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        responses=GET_CUSTOMER_SINGLE['response'],
        operation_description="API to get particular customer",
        manual_parameters=GET_CUSTOMER_SINGLE['params'],
        tags=["customer"]
    )
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(HTTP_404, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses=PUT_CUSTOMER_SINGLE['response'],
        operation_description="API to modify specific customer details",
        manual_parameters=PUT_CUSTOMER_SINGLE['params'],
        request_body=PUT_CUSTOMER_SINGLE['request_body'],
        tags=["customer"]
    )
    def put(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(HTTP_404, status=status.HTTP_404_NOT_FOUND)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses=DELETE_CUSTOMER_SINGLE['response'],
        operation_description="API to delete particular customer",
        manual_parameters=DELETE_CUSTOMER_SINGLE['params'],
        tags=["customer"]
    )
    def delete(self, request, pk):
        try:
            customer = Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            return Response(HTTP_404, status=status.HTTP_404_NOT_FOUND)
        customer.delete()
        return Response(HTTP_204_DELETE, status=status.HTTP_204_NO_CONTENT)


class GetPostCustomer(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @swagger_auto_schema(
        operation_description="API to Get all customers",
        tags=["customer"]
    )
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="API to Create new customers",
        responses=POST_CUSTOMER['response'],
        request_body=POST_CUSTOMER['request_body'],
        tags=["customer"]
    )
    def post(self, request):
        data = {
            "name": request.data.get("name"),
            "first_name": request.data.get('first_name'),
            "last_name": request.data.get('last_name'),
            "age": int(request.data.get('age')),
            "email": request.data.get("email")
        }
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,  status=status.HTTP_400_BAD_REQUEST)
