import json

from django.test import Client, TestCase, client
from django.urls import reverse
from rest_framework import status

from ..models import Customer
from ..serializers import CustomerSerializer

client = Client()


class GetAllCustomersTest(TestCase):
    """
    Test module for GET all customers API
    """

    def setUp(self) -> None:
        Customer.objects.create(name="John Doe", first_name="John",
                                last_name="Doe", age=24, email='john.doe@xyz.com')
        Customer.objects.create(name="David Williams", first_name="David",
                                last_name="Williams", age=32,
                                email='david.williams@xyz.com')
        Customer.objects.create(name="John Jones", first_name="John",
                                last_name="Jones", age=24, email='john.jones@xyz.com')
        Customer.objects.create(name="Tracey Smith", first_name="Tracey",
                                last_name="Smith", age=32,
                                email='tracy.smith@xyz.com')

    def test_get_all_customers(self):
        response = client.get(reverse('get_post_customer'))
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCustomerTest(TestCase):
    """
    Test module for GET single customer API
    """

    def setUp(self) -> None:
        self.john = Customer.objects.create(name="John Doe", first_name="John",
                                            last_name="Doe", age=24, email='john.doe@xyz.com')
        self.david = Customer.objects.create(name="David Williams", first_name="David",
                                             last_name="Williams", age=32,
                                             email='david.williams@xyz.com')
        self.jones = Customer.objects.create(name="John Jones", first_name="John",
                                             last_name="Jones", age=24, email='john.jones@xyz.com')
        self.tracey = Customer.objects.create(name="Tracey Smith", first_name="Tracey",
                                              last_name="Smith", age=32,
                                              email='tracy.smith@xyz.com')

    def test_get_valid_single_customer(self):
        response = client.get(
            reverse("get_delete_update_customer", kwargs={'pk': self.john.pk}))
        customer = Customer.objects.get(pk=self.john.pk)
        serializer = CustomerSerializer(customer)
        self.assertEqual(serializer.data, response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_customer(self):
        response = client.get(
            reverse('get_delete_update_customer', kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCustomerTest(TestCase):
    """
    Test module for POST customer API
    """

    def setUp(self) -> None:
        self.valid = {
            "name": "John Doe",
            "first_name": "John",
            "last_name": "Doe",
            "age": 32,
            "email": "john.doe@xyz.com"
        }
        self.invalid = {
            "name": "",
            "first_name": "John",
            "last_name": "Doe",
            "age": 32,
            "email": "john.doe@xyz.com"
        }

    def test_create_valid_customer(self):
        response = client.post(reverse("get_post_customer"),
                               data=json.dumps(self.valid),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_customer(self):
        response = client.post(reverse("get_post_customer"),
                               data=json.dumps(self.invalid),
                               content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleCustomer(TestCase):
    """
    Test module for PUT customer API
    """

    def setUp(self) -> None:
        self.john = Customer.objects.create(name="John Doe", first_name="John",
                                            last_name="Doe", age=24, email='john.doe@xyz.com')
        self.david = Customer.objects.create(name="David Williams", first_name="David",
                                             last_name="Williams", age=32,
                                             email='david.williams@xyz.com')

        self.valid_payload = {
            "name": "John Doe",
            "first_name": "John",
            "last_name": "Doe",
            "age": 12,
            "email": "john.doe@xyz.com"
        }
        self.invalid_payload = {
            "name": "",
            "first_name": "David",
            "last_name": "Williams",
            "age": 22,
            "email": "david.williams@xyz.com"
        }

    def test_valid_customer_update(self):
        response = client.put(
            reverse('get_delete_update_customer', kwargs={"pk": self.john.pk}),
            data=json.dumps(self.valid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_customer(self):
        response = client.put(reverse('get_delete_update_customer', kwargs={"pk": self.david.pk}),
                              data=json.dumps(self.invalid_payload), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSingleCustomer(TestCase):
    """
    Test module for DELETE API
    """

    def setUp(self) -> None:
        self.john = Customer.objects.create(name="John Doe", first_name="John",
                                            last_name="Doe", age=24, email='john.doe@xyz.com')
        self.david = Customer.objects.create(name="David Williams", first_name="David",
                                             last_name="Williams", age=32,
                                             email='david.williams@xyz.com')

    def test_delete_valid_customer(self):
        response = client.delete(
            reverse("get_delete_update_customer", kwargs={"pk": self.john.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_customer(self):
        response = client.delete(
            reverse("get_delete_update_customer", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
