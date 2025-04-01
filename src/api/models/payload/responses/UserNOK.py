from ninja import ModelSchema

from src.api.models.postgres import UserNextOfKin


class UserNOKResponse(ModelSchema):
    class Meta:
        model = UserNextOfKin
        fields = (
            "id",
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "address",
            "relationship",
        )
        fields_optional = (
            "first_name",
            "last_name",
            "phone_number",
            "email",
            "address",
            "relationship",
        )
