import os
from typing import List

from pydantic import BaseSettings
from pydantic.networks import AnyHttpUrl
from sqlalchemy import URL
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Main
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    PROJECT_DSC: str = os.getenv("PROJECT_DESCRIPTION")

    API_HOST: str = os.getenv("API_HOST")
    API_PORT: int = os.getenv("API_PORT")

    API_V1_STR: str = os.getenv("API_URL")
    API_LOG_LVL: str = os.getenv("LOG_LVL")
    API_RELOAD: bool = os.getenv("RELOAD")
    API_VS: str = os.getenv("API_VERSION")
    API_DBG: bool = os.getenv("API_DEBUG")
    OPEN_API_URL: str = f"{API_V1_STR}/openapi.json"

    BOT_TOKEN: str = os.environ["BOT_TOKEN"]
    GPT_ENDPOINT_URL: str = os.environ["ENDPOINT_URL"]
    WEB_APP_URL: str = os.environ["WEB_APP_URL"]
    DEVICE_ID: str = os.environ["DEVICE_ID"]

    DB_NAME: str = os.getenv("DATABASE_NAME")
    DB_USER: str = os.getenv("DATABASE_USER")
    DB_PWD: str = os.getenv("DATABASE_PASSWORD")
    DB_HOST: str = os.getenv("DATABASE_HOST")
    DB_PORT: int = os.getenv("DATABASE_PORT")
    DB_ADR: str = os.getenv("DATABASE_ADAPTER")
    DB_URL: str = str(f"{DB_ADR}://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}")

    URL = URL.create(
        DB_ADR,
        username=DB_USER,
        password=DB_PWD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

    EMAIL_TEST_USER: str = "test@example.com"
    FIRST_SUPERUSER: str = os.getenv("SU_USERNAME")
    FIRST_SUPERUSER_EMAIL: str = os.getenv("SU_USER_EMAIL")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("SU_USER_PASS")
    USERS_OPEN_REGISTRATION: bool = True

    SU_USERNAME = os.environ["SU_USERNAME"]
    SU_USER_EMAIL = os.environ["SU_USER_EMAIL"]
    SU_USER_PASS = os.environ["SU_USER_PASS"]

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWD_ALG")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # Celery
    BROKER: str = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = os.getenv("CELERY_BROKER_URL")

    # SMTP
    SMTP_HOST: str = os.getenv("SMTP_HOST")
    SMTP_PORT: int = os.getenv("SMTP_PORT")
    SMTP_EMAIL_FROM: str = os.getenv("SMTP_EMAIL_FROM")
    SMTP_EMAIL_FROM_PASSWD: str = os.getenv("SMTP_EMAIL_FROM_PASSWD")
    SMTP_TLS: bool = os.getenv("SMTP_TLS")

    TEMPLATES_DIR: str = "/app/templates"

    class Config:
        case_sensitive = True


settings = Settings()
