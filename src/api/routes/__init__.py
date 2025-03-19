from ninja import NinjaAPI
from django.http import HttpRequest

from src import __version__ as version

api = NinjaAPI(version=version)


@api.get("/")
def home(request: HttpRequest) -> dict:
    return {"message": "Hello, World!"}


from src.api.middlewares.AppMiddleware import Authentication  # noqa: E402

api.add_router("/auth", "src.api.routes.Auth.router", tags=["Auth"])
api.add_router(
    "/users", "src.api.routes.User.router", auth=Authentication(), tags=["User"]
)
api.add_router(
    "/withdrawal-accounts",
    "src.api.routes.WithdrawalAccount.router",
    auth=Authentication(),
    tags=["User"],
)
