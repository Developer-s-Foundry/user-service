from ninja import NinjaAPI
from django.http import HttpRequest
from ninja.openapi.schema import OpenAPISchema

from src.env import app
from src.api.middlewares.GateWayMiddleware import authentication, add_global_headers

api: NinjaAPI = NinjaAPI(
    version=app["version"],
    title=app["display_name"],
    description=app["description"],
    auth=authentication,
)

original_get_openapi_schema = api.get_openapi_schema


def custom_openapi_schema(path_params: dict| None =None) -> OpenAPISchema:
    schema = original_get_openapi_schema()

    schema["components"]["securitySchemes"] = {
        "Gateway Key": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-GATEWAY-KEY",
        },
        "API Timestamp": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-GATEWAY-TIMESTAMP",
        },
        "API Signature": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-GATEWAY-SIGNATURE",
        },
        "User ID": {
            "type": "apiKey",
            "in": "header",
            "name": "X-USER-ID",
        },
        "User Email": {
            "type": "apiKey",
            "in": "header",
            "name": "X-USER-EMAIL",
        },
    }

    schema["security"] = [
        {
            "Gateway Key": [],
            "API Timestamp": [],
            "API Signature": [],
            "User ID": [],
            "User Email": [],
        }
    ]

    schema = add_global_headers(schema)
    return schema


setattr(api, "get_openapi_schema", custom_openapi_schema)

from src.api.utils import error_handlers  # noqa: E402, F401


@api.get("/", auth=None)
async def home(request: HttpRequest) -> dict:
    return {"message": "Hello, World!"}


api.add_router("/users", "src.api.routes.User.router", tags=["User"])
api.add_router("/kyc", "src.api.routes.UserKYC.router", tags=["User KYC"])
api.add_router(
    "/next-of-kin",
    "src.api.routes.UserNOK.router",
    tags=["User NOK"],
)
api.add_router(
    "/withdrawal-accounts",
    "src.api.routes.WithdrawalAccount.router",
    tags=["User"],
)
