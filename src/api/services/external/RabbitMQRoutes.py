from src.config.asgi import broker

from ..UserService import UserRouter

broker.include_router(UserRouter)