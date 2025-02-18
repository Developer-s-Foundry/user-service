from src.env import env, cache

redis = cache.get("redis")
redis_scheme = "rediss://" if (not env.isLocal and not env.isTest) else "redis://"

REDIS = {
    "BACKEND": "django.core.cache.backends.redis.RedisCache",
    "LOCATION": f"{redis_scheme}"
    f"{user if (user := redis['user']) else ''}"
    f"{f':{pas}@' if (pas := redis['pass']) else ''}"
    f"{host if (host := redis['host']) else ''}"
    f"{f':{port}' if (port := redis['port']) else ''}",
    "KEY_PREFIX": "df_w",
}
