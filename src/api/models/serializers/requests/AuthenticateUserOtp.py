from rest_framework import serializers


class AuthenticateUserOtp(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
