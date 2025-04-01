from ninja import ModelSchema

from src.api.models.postgres import UserKYCInformation


class UserKYCResponse(ModelSchema):
    class Meta:
        model = UserKYCInformation
        fields = (
            "id",
            "bvn",
            "is_bvn_verified",
            "document_type",
            "document_id",
            "is_document_verified",
        )
        fields_optional = (
            "bvn",
            "is_bvn_verified",
            "document_type",
            "document_id",
            "is_document_verified",
        )
