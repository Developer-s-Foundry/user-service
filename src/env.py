from typing import Any

from src import __name__, __version__
from src.utils.env import get_env_variable


class Env:
    @property
    def isLocal(self) -> bool:
        return get_env_variable("ENVIRONMENT") == "local"

    @property
    def isTest(self) -> bool:
        return get_env_variable("ENVIRONMENT") == "test"

    @property
    def isProd(self) -> bool:
        return get_env_variable("ENVIRONMENT") == "prod"


env = Env()

app: dict[str, str | bool | dict[str, list]] = {
    "name": __name__,
    "version": __version__,
    "secret_key": get_env_variable("SECRET_KEY"),
    "debug": True if (env.isLocal or env.isTest) else False,
    "allowed_hosts": get_env_variable(
        "ALLOWED_HOSTS", default="*", cast=lambda x: [v.strip() for v in x.split(",")]
    ),
}

log: dict[str, Any] = {
    "level": get_env_variable("LOG_LEVEL", default="debug", cast=lambda x: x.upper()),
}

db: dict[str, dict[str, str | int]] = {
    "mongo": {
        "host": get_env_variable("MONGODB_HOST"),
        "port": get_env_variable("MONGODB_PORT", cast=int),
        "user": get_env_variable("MONGODB_USERNAME"),
        "pass": get_env_variable("MONGODB_PASSWORD"),
        "database": get_env_variable("MONGODB_DATABASE"),
    },
    "pg": {
        "host": get_env_variable("PG_HOST"),
        "port": get_env_variable("PG_PORT", cast=int),
        "user": get_env_variable("PG_USERNAME"),
        "pass": get_env_variable("PG_PASSWORD"),
        "database": get_env_variable("PG_DATABASE"),
    },
}

cache: dict[str, dict[str, str | int]] = {
    "redis": {
        "host": get_env_variable("REDIS_HOST"),
        "port": get_env_variable("REDIS_PORT", cast=int),
        "user": get_env_variable("REDIS_USERNAME"),
        "pass": get_env_variable("REDIS_PASSWORD"),
    }
}


jwt_config: dict[str, Any] = {
    "secret": get_env_variable("JWT_SECRET"),
    "issuer": get_env_variable("JWT_ISSUER"),
}
