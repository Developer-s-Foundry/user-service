from rest_framework import serializers
from django.contrib.auth.password_validation import (
    MinimumLengthValidator,
    NumericPasswordValidator,
)


class AuthenticateUserRequest(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(
        validators=[MinimumLengthValidator(8), NumericPasswordValidator()]
    )
