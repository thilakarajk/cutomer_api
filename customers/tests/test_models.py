from django.test import TestCase

from ..models import Customer

# Create your tests here.


class CustomerTest(TestCase):
    """
    Test Module for Customer module
    """

    def setUp(self) -> None:
        Customer.objects.create(name="John Doe", first_name="John",
                                last_name="Doe", age=24, email='john.doe@xyz.com')
        Customer.objects.create(name="David Williams", first_name="David",
                                last_name="Williams", age=32,
                                email='david.williams@xyz.com')

    def test_customer_details(self):
        customer_john = Customer.objects.get(first_name="John")
        customer_david = Customer.objects.get(first_name="David")
        self.assertEqual(customer_john.get_details(),
                         "John's email ID: john.doe@xyz.com")
        self.assertEqual(customer_david.get_details(),
                         "David's email ID: david.williams@xyz.com")
