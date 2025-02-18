from src.utils import get_env_variable


class Env:
    @property
    def isLocal(self):
        return get_env_variable("ENVIRONMENT") == "local"

    @property
    def isTest(self):
        return get_env_variable("ENVIRONMENT") == "test"

    @property
    def isProd(self):
        return get_env_variable("ENVIRONMENT") == "prod"


env = Env()

app = {
    "secret_key": get_env_variable("SECRET_KEY"),
    "debug": True if (env.isLocal or env.isTest) else False,
    "allowed_hosts": get_env_variable(
        "ALLOWED_HOSTS", default="*", cast=lambda x: [v.strip() for v in x.split(",")]
    ),
}

db = {
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

cache = {
    "redis": {
        "host": get_env_variable("REDIS_HOST"),
        "port": get_env_variable("REDIS_PORT", cast=int),
        "user": get_env_variable("REDIS_USERNAME"),
        "pass": get_env_variable("REDIS_PASSWORD"),
    }
}
