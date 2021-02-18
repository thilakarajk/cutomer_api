from rest_framework import serializers

from .models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ("name", "first_name", "last_name", "age",
                  "email", "created_at", "updated_at", "id")
