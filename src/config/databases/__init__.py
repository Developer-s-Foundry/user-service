from .mongo import MONGO
from .postgres import POSTGRES

DATABASES = {
    "default": {},
    "pg": POSTGRES,
    "mongo": MONGO,
}

DATABASE_ROUTERS = ["src.config.databases.router.DatabaseRouter"]
