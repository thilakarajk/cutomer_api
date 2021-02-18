from django.db import models


# Create your models here.
class Customer(models.Model):
    """
    Customer model
    Defines the customer attributes
    """
    name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    email = models.CharField(max_length=255)

    def __repr__(self) -> str:
        return f'{self.name} is added'

    def get_details(self):
        return f"{self.first_name}'s email ID: {self.email}"
