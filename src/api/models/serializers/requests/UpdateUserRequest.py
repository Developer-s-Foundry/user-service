from rest_framework import serializers


class UpdateUserRequest(serializers.Serializer):
    id: str = ""
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    address = serializers.CharField()
    phone_number = serializers.CharField()
    state_lga_id = serializers.IntegerField(min_value=1)

    def validate(self, data: dict) -> dict:
        data["id"] = self.id
        return data
