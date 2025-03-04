from rest_framework import serializers
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    NumericPasswordValidator,
)


class CreateUserRequest(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        validators=[MinimumLengthValidator(8), NumericPasswordValidator()]
    )
    address = serializers.CharField()
    phone_number = serializers.CharField()
    state_lga_id = serializers.IntegerField(min_value=1)
