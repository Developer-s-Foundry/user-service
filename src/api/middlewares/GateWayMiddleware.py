import hmac
import hashlib
from datetime import datetime, timedelta

from django.http import HttpRequest
from ninja.errors import AuthenticationError
from ninja.security import APIKeyHeader
from ninja.openapi.schema import OpenAPISchema

from src.env import api_gateway
from src.utils.logger import Logger


class GateWayAuth(APIKeyHeader):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        super().__init__()

    def authenticate(self, request: HttpRequest, key: str | None) -> str | None:
        try:
            api_key = request.headers["X-API-GATEWAY-KEY"]
            api_timestamp = request.headers["X-API-GATEWAY-TIMESTAMP"]
            api_signature = request.headers["X-API-GATEWAY-SIGNATURE"]
            user_id = request.headers["X-USER-ID"]
            user_email = request.headers["X-USER-EMAIL"]
        except KeyError as e:
            message = f"Missing required header: {e}"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"headers": request.headers},
                }
            )
            raise AuthenticationError(message=message)

        valid_api_key = api_gateway["key"]
        if api_key != valid_api_key:
            message = "Invalid API key!"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"headers": request.headers},
                }
            )
            raise AuthenticationError(message=message)

        self._verify_signature(valid_api_key, api_signature, api_timestamp)

        self.logger.debug(
            {
                "activity_type": "Authenticate User",
                "message": "Successfully authenticated user",
                "metadata": {
                    "user_id": user_id,
                    "user_email": user_email,
                },
            }
        )
        setattr(request, "auth_email", user_email)
        setattr(request, "auth_id", user_id)

        return api_signature

    def _verify_signature(
        self, valid_api_key: str, signature: str, timestamp: str
    ) -> bool:
        valid_signature = self.generate_signature(valid_api_key, timestamp)
        is_valid = hmac.compare_digest(valid_signature, signature)

        if not is_valid:
            message = "Invalid signature!"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"signature": signature},
                }
            )
            raise AuthenticationError(message=message)

        initial_time = datetime.fromtimestamp(int(timestamp) / 1000)
        valid_window = initial_time + timedelta(minutes=api_gateway["expires_at"])
        if valid_window < datetime.now():
            message = "Signature expired!"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"timestamp": timestamp},
                }
            )
            raise AuthenticationError(message=message)

        return True

    def generate_signature(self, api_key: str, timestamp: str) -> str:
        signature = hmac.new(
            key=api_key.encode(), msg=timestamp.encode(), digestmod=hashlib.sha256
        ).hexdigest()
        return signature


def get_authentication() -> GateWayAuth:
    gateway_auth = GateWayAuth(Logger("Authentication"))
    return gateway_auth


def add_global_headers(schema: OpenAPISchema) -> OpenAPISchema:
    for path in schema["paths"]:
        for method in schema["paths"][path]:
            operation = schema["paths"][path][method]
            if operation.get("security"):
                operation["security"] = schema["security"]
    return schema


authentication = get_authentication()
