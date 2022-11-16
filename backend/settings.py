from os import environ

from passlib.context import CryptContext


def get_env_with_context(value: str, default=None, context="API") -> str:
    return environ.get(f"{context}_{value}")


class Settings:
    APP_TITLE = "Currency Converter API"
    SECRET_KEY = environ.get("SECRET_KEY")
    DB_USER = get_env_with_context("USER", context="POSTGRES")
    DB_PASSWORD = get_env_with_context("PASSWORD", context="POSTGRES")
    DB_DB = get_env_with_context("DB", context="POSTGRES")
    DB_PORT = get_env_with_context("PORT", context="POSTGRES")
    DB_HOST = get_env_with_context("HOST", context="POSTGRES")
    DB_URL = environ.get(
        "DATABASE_URL",
        f"postgresql+psycopg2://"
        f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DB}",
    ).replace("postgres://", "postgresql://")
    TEST_DB = get_env_with_context("TEST_DB", context="POSTGRES")
    TEST_DB_URL = (
        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB}"
    )
    ACCESS_TOKEN_EXPIRY_TIME = 60 * 30
    REFRESH_TOKEN_EXPIRY_TIME = 60 * 24 * 7
    PASSWORD_HASHER = CryptContext(schemes=["bcrypt"], deprecated="auto")
    JWT_ALGORITHM = "HS256"
    REDIS_URL = environ.get("REDIS_URL")
    CURRENCY_CACHE_EXPIRY_TIME = 60 * 60 * 24
    PAGE_SIZE = 50
    ALLOWED_CLIENTS = environ.get("ALLOWED_CLIENTS").split()


settings = Settings()
