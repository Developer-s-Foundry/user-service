from src.env import log

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "": {
            "level": log["level"],
            "handlers": ["console"],
        },
    },
    "formatters": {
        "verbose": {
            "format": ("=" * 20) + "\n{asctime} {levelname} {module}\n{message}\n\n",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
}
