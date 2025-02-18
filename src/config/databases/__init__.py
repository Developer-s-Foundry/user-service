from .mongo import MONGO
from .postgres import POSTGRES

DATABASES = {
    "default": {},
    "pg": POSTGRES,
    "mongo": MONGO,
}
