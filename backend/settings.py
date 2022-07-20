from os import environ

from passlib.context import CryptContext


def get_env_with_context(value: str, default=None, context="API") -> str:
    return environ.get(f"{context}_{value}")


class Settings:
    APP_TITLE = "Currency Converter API"
    ALLOWED_HOST = environ.get("ALLOWED_HOST")
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = bool(environ.get("DEBUG"))
    ALLOWED_PORT = 8000
    DB_USER = get_env_with_context("USER", context="POSTGRES")
    DB_PASSWORD = get_env_with_context("PASSWORD", context="POSTGRES")
    DB_DB = get_env_with_context("DB", context="POSTGRES")
    DB_PORT = get_env_with_context("PORT", context="POSTGRES")
    DB_HOST = get_env_with_context("HOST", context="POSTGRES")
    DB_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}"
    )
    ACCESS_TOKEN_EXPIRY_TIME = 60 * 30
    REFRESH_TOKEN_EXPIRY_TIME = 60 * 24 * 7
    PASSWORD_HASHER = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_ALGORITHM = "HS256"
    REDIS_HOST = get_env_with_context("HOST", default="localhost", context="REDIS")
    REDIS_PORT = get_env_with_context("PORT", default="6379", context="REDIS")
    CURRENCY_CACHE_EXPIRY_TIME = 60 * 60 * 24
    PAGE_SIZE = 50


settings = Settings()
