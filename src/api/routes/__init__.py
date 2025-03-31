from ninja import NinjaAPI
from django.http import HttpRequest

from src.env import app
from src.utils.svcs import Depends
from src.api.middlewares.AppMiddleware import Authentication

api: NinjaAPI = NinjaAPI(
    version=app["version"],
    title=app["display_name"],
    description=app["description"],
)

from src.api.utils import error_handlers  # noqa: E402, F401


@api.get("/")
def home(request: HttpRequest) -> dict:
    return {"message": "Hello, World!"}


authentication = Depends(Authentication)

api.add_router("/auth", "src.api.routes.Auth.router", tags=["Auth"])
api.add_router(
    "/users", "src.api.routes.User.router", auth=authentication, tags=["User"]
)
api.add_router(
    "/withdrawal-accounts",
    "src.api.routes.WithdrawalAccount.router",
    auth=authentication,
    tags=["User"],
)
api.add_router(
    "/password/reset", "src.api.routes.PasswordReset.router", tags=["Password"]
)
