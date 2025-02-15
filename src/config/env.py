from functools import cache
from pathlib import Path
from decouple import config as decouple_config, Config, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


@cache
def get_environment():
    if ENV_FILE.exists():
        return Config(RepositoryEnv(ENV_FILE))
    return decouple_config


get_env_var = get_environment()
