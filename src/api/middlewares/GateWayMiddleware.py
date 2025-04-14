import base64
import hashlib
import hmac
from datetime import datetime
from http import HTTPStatus

from django.http import HttpRequest
from ninja.errors import HttpError
from ninja.openapi.schema import OpenAPISchema
from ninja.security import APIKeyHeader
from src.env import api_gateway
from src.utils.logger import Logger


class GateWayAuth(APIKeyHeader):
    def __init__(self, logger: Logger) -> None:
        self.logger = logger
        # self.param_name = 'X-API-GATEWAY-KEY'
        super().__init__()

    def authenticate(self, request: HttpRequest, api_key: str):
        api_key = request.headers.get('X-API-GATEWAY-KEY')
        api_timestamp = request.headers.get('X-API-GATEWAY-TIMESTAMP')
        api_signature = request.headers.get('X-API-GATEWAY-SIGNATURE')
        user_id = request.headers.get('X-USER-ID')
        user_email = request.headers.get('X-USER-EMAIL')

        if not all([api_key, api_timestamp, api_signature, user_id, user_email]):
            message = "Missing required headers!"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"headers": request.headers},
                }
            )
            raise HttpError(HTTPStatus.UNAUTHORIZED, message)
        
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
            raise HttpError(HTTPStatus.UNAUTHORIZED, message)
    
        self._verify_signature(valid_api_key, valid_api_key, api_timestamp)

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

        
    

    def _verify_signature(self, valid_api_key: str, signature: str, timestamp: str) -> bool:
    
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
            raise HttpError(HTTPStatus.UNAUTHORIZED, message)


        timestamp = int(timestamp)
        current_time = datetime.now().timestamp() * 1000
        lifespan = api_gateway['expires_at'] * 60 * 60 * 1000; 

        if abs(current_time - timestamp) > lifespan:
            message = "Signature expired!"
            self.logger.error(
                {
                    "activity_type": "Authenticate User",
                    "message": message,
                    "metadata": {"timestamp": timestamp},
                }
            )
            raise HttpError(HTTPStatus.UNAUTHORIZED, message)

        return True


    def generate_signature(self, api_key: str, timestamp: str) -> str:
        signature = hmac.new(
            key=api_key.encode(),
            msg=timestamp.encode(),
            digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')


def get_authentication() -> GateWayAuth:
    gateway_auth = GateWayAuth(Logger("Authentication"))
    return gateway_auth

def add_global_headers(schema: OpenAPISchema):
    for path in schema["paths"]:
        for method in schema["paths"][path]:
            operation = schema["paths"][path][method]
            if operation.get("security"):
                operation["security"] = schema["security"]
    return schema


authentication = get_authentication()



