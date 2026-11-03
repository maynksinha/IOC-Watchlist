import os
from pathlib import Path

from dotenv import load_dotenv

from app.constants import EnvFilePath

_root = Path(__file__).parent.parent.parent
_env_file = _root / EnvFilePath.ENV.value
_default_env_file = _root / EnvFilePath.DEFAULT.value

load_dotenv(_env_file if _env_file.exists() else _default_env_file)

DATABASE_URL: str = os.getenv("DATABASE_URL")
CORS_ORIGINS: str = os.getenv("CORS_ORIGINS")
ENV: str = os.getenv("ENV")
HOST: str = os.getenv("HOST")
PORT: int = int(os.getenv("PORT"))

IS_PROD: bool = ENV == "production"
CORS_ORIGINS_LIST: list[str] = [o.strip() for o in CORS_ORIGINS.split(",")]
