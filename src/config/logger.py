from src.env import log

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "df_wallet": {
            "level": log["level"],
            "handlers": ["console", "combined_file", "error_file"],
        },
    },
    "formatters": {
        "verbose": {
            "format": "{asctime} [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "combined_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/combined/combined.log",
            "when": "D",
            "formatter": "verbose",
        },
        "error_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/error/error.log",
            "when": "D",
            "formatter": "verbose",
            "level": "ERROR",
        },
    },
}
