from ninja import NinjaAPI
from django.http import HttpRequest

from src.env import app
from src.api.middlewares.AppMiddleware import authentication

api: NinjaAPI = NinjaAPI(
    version=app["version"],
    title=app["display_name"],
    description=app["description"],
)

from src.api.utils import error_handlers  # noqa: E402, F401


@api.get("/")
async def home(request: HttpRequest) -> dict:
    return {"message": "Hello, World!"}


api.add_router("/auth", "src.api.routes.Auth.router", tags=["Auth"])
api.add_router(
    "/password/reset", "src.api.routes.PasswordReset.router", tags=["Password"]
)
api.add_router(
    "/users", "src.api.routes.User.router", auth=authentication, tags=["User"]
)
api.add_router(
    "/kyc", "src.api.routes.UserKYC.router", auth=authentication, tags=["User KYC"]
)
api.add_router(
    "/next-of-kin",
    "src.api.routes.UserNOK.router",
    auth=authentication,
    tags=["User NOK"],
)
api.add_router(
    "/withdrawal-accounts",
    "src.api.routes.WithdrawalAccount.router",
    auth=authentication,
    tags=["User"],
)
