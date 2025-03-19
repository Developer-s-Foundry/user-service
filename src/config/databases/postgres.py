from src.env import db, env

pg = db["pg"]

POSTGRES = {
    "NAME": pg["database"],
    "ENGINE": "django.db.backends.postgresql",
    "USER": pg["user"],
    "PASSWORD": pg["pass"],
    "HOST": pg["host"],
    "PORT": pg["port"],
    "OPTIONS": {
        "sslmode": "require" if (not env.isLocal and not env.isTest) else "prefer",
    },
}
